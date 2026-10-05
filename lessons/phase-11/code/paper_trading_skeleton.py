"""
自動化交易系統骨架（教學用，只做紙上交易）
==========================================
資料 → 訊號 → 風控 → 下單 → 監控，每個模組各自獨立，方便替換與測試。

⚠️ 這是教學用的骨架：PaperBroker 只是模擬成交，不會連接任何真實券商。
   真實券商 API 的介面、規則與風險差異很大，接上實盤前必須經過 Phase 12 的完整流程。
"""
import logging
from dataclasses import dataclass, field

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("bot")


# ---------------------------------------------------------------- 1. 資料
class DataFeed:
    """一天一天地提供資料，模擬「每天收盤後拿到新資料」。"""

    def __init__(self, path):
        self.df = pd.read_csv(path, parse_dates=["Date"], index_col="Date")

    def __iter__(self):
        for i in range(len(self.df)):
            yield self.df.index[i], self.df.iloc[: i + 1]      # 只給到今天為止的資料


# ---------------------------------------------------------------- 2. 訊號
class MaStrategy:
    def __init__(self, fast=50, slow=200):
        self.fast, self.slow = fast, slow

    def target_position(self, history):
        """回傳目標部位：1 = 持有、0 = 空手。資料不足時回傳 None。"""
        close = history["Close"]
        if len(close) < self.slow:
            return None
        return 1 if close.iloc[-self.fast:].mean() > close.iloc[-self.slow:].mean() else 0


# ---------------------------------------------------------------- 3. 風控
@dataclass
class RiskManager:
    max_position_pct: float = 1.0       # 單一部位上限（佔總資產）
    max_drawdown_stop: float = 0.25     # 帳戶回撤超過 25% → 停機（kill switch）
    peak_equity: float = 0.0
    halted: bool = False

    def check(self, equity):
        self.peak_equity = max(self.peak_equity, equity)
        drawdown = equity / self.peak_equity - 1
        if not self.halted and drawdown < -self.max_drawdown_stop:
            self.halted = True
            log.warning(f"⛔ 回撤 {drawdown:.1%} 超過上限，系統停機，等待人工檢查")
        return not self.halted


# ---------------------------------------------------------------- 4. 下單（紙上交易）
@dataclass
class PaperBroker:
    cash: float = 1_000_000
    shares: int = 0
    buy_cost: float = 0.000855
    sell_cost: float = 0.003855
    pending: list = field(default_factory=list)
    fills: list = field(default_factory=list)

    def submit(self, side, date):
        if self.pending:                                         # 防止重複下單
            log.info(f"{date.date()} 已有未成交委託，略過")
            return
        self.pending.append(side)

    def execute_at_open(self, date, open_price):
        """在今天開盤處理昨天的委託。"""
        for side in self.pending:
            if side == "buy" and self.shares == 0:
                self.shares = int(self.cash / (open_price * (1 + self.buy_cost)))
                self.cash -= self.shares * open_price * (1 + self.buy_cost)
            elif side == "sell" and self.shares > 0:
                self.cash += self.shares * open_price * (1 - self.sell_cost)
                self.shares = 0
            self.fills.append((date, side, open_price))
            log.info(f"{date.date()} 成交 {side} @ {open_price:.2f}")
        self.pending.clear()

    def equity(self, price):
        return self.cash + self.shares * price


# ---------------------------------------------------------------- 5. 主迴圈 + 監控
def run(path="sample_long.csv", max_drawdown_stop=0.25, verbose=True):
    log.setLevel(logging.INFO if verbose else logging.WARNING)
    feed, strategy, broker = DataFeed(path), MaStrategy(), PaperBroker()
    risk = RiskManager(max_drawdown_stop=max_drawdown_stop)
    equity_curve = []
    for date, history in feed:
        today = history.iloc[-1]
        broker.execute_at_open(date, today["Open"])              # ① 開盤：執行昨天的委託
        equity = broker.equity(today["Close"])                   # ② 收盤：計算資產
        equity_curve.append((date, equity))
        if not risk.check(equity):                               # ③ 風控檢查
            if broker.shares > 0:
                broker.submit("sell", date)
            continue
        target = strategy.target_position(history)               # ④ 產生訊號
        if target == 1 and broker.shares == 0:
            broker.submit("buy", date)
        elif target == 0 and broker.shares > 0:
            broker.submit("sell", date)
    curve = pd.Series(dict(equity_curve))
    log.warning(f"結束：最終資產 {curve.iloc[-1]:,.0f}，共成交 {len(broker.fills)} 次")
    return curve, broker


if __name__ == "__main__":
    run()
