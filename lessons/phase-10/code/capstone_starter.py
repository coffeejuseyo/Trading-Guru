"""
Phase 10 綜合專案：起始程式
==========================
把 Phase 8 的 3 份規格書寫成訊號函式，用同一套流程回測、檢驗、產生報告數字。

使用方式：
1. 把 DATA_FILE 換成你在 9.10 下載、9.11 清理過的真實資料（使用還原價格）
2. 依照你的規格書修改三個 signal_xxx() 函式
3. 執行：python capstone_starter.py
4. 把輸出的數字填進 templates/backtest-report.md

⚠️ 範例訊號是 8.3、8.4、8.5 的簡化版，只做多、全額進出，請依你的規格書調整。
"""
import numpy as np
import pandas as pd
from bt_toolkit import (load_prices, sma, rsi, atr, state_signal, backtest,
                        tw_costs, perf_stats, extract_trades, trade_stats)

DATA_FILE = "sample_long.csv"     # ← 換成你的資料
OOS_START = "2019"                 # ← 研究開始前就決定，之後不要改
COSTS = tw_costs()                 # ← 依你的券商與商品調整（ETF 可用 tax_rate=0.001）


# ---------------------------------------------------------------- 三份規格書的訊號
def signal_trend(df):
    """趨勢（8.3 範例 B 簡化）：收盤突破過去 55 日最高價進場；跌破過去 20 日最低價出場。"""
    entry = df["Close"] > df["High"].rolling(55).max().shift(1)
    exit_ = df["Close"] < df["Low"].rolling(20).min().shift(1)
    return state_signal(entry, exit_)


def signal_mean_reversion(df):
    """均值回歸（8.5 範例 A）：收盤 > 200 日均線且 RSI(2) < 10 進場；收盤 > 5 日均線或持有滿 10 天出場。"""
    entry = (rsi(df["Close"], 2) < 10) & (df["Close"] > sma(df["Close"], 200))
    exit_ = df["Close"] > sma(df["Close"], 5)
    return state_signal(entry, exit_, max_days=10)


def signal_breakout(df):
    """突破（8.4 簡化）：波動收斂（ATR/收盤 在過去 120 日的最低 25%）後，收盤創 50 日新高進場；
    收盤跌破 20 日均線出場。"""
    atr_pct = atr(df, 20) / df["Close"]
    quiet = atr_pct.rolling(120).rank(pct=True).shift(1) <= 0.25
    entry = quiet & (df["Close"] > df["Close"].rolling(50).max().shift(1))
    exit_ = df["Close"] < sma(df["Close"], 20)
    return state_signal(entry, exit_)


STRATEGIES = {
    "趨勢": signal_trend,
    "均值回歸": signal_mean_reversion,
    "突破": signal_breakout,
}


# ---------------------------------------------------------------- 檢驗流程
def evaluate(df, name, signal_func):
    signal = signal_func(df)
    res = backtest(df, signal, *COSTS)
    bh = df["Close"].pct_change().fillna(0)
    exposure = res["pos"].mean()
    matched = backtest(df, pd.Series(exposure, index=df.index))["strat_ret"]

    print(f"\n==================== {name} ====================")
    rows = {
        "樣本內": res["strat_ret"].loc[:str(int(OOS_START) - 1)],
        "樣本外": res["strat_ret"].loc[OOS_START:],
        "全期間": res["strat_ret"],
        "買進持有（全期間）": bh,
        f"曝險相當 {exposure:.0%}（全期間）": matched,
    }
    for label, r in rows.items():
        p = perf_stats(r)
        print(f"{label:<16} 年化 {p['年化報酬']:>7.2%}  最大回撤 {p['最大回撤']:>8.2%}  夏普 {p['夏普比率']:>5.2f}")

    s = trade_stats(extract_trades(df, res))
    print(f"交易 {s['交易次數']} 筆，勝率 {s['勝率']:.1%}，盈虧比 {s['盈虧比']:.2f}，"
          f"期望值 {s['每筆期望值']:.2%}，最大連虧 {s['最大連虧']}")

    b, sc = COSTS
    double = perf_stats(backtest(df, signal, 2 * b, 2 * sc)["strat_ret"])["夏普比率"]
    delay = perf_stats(backtest(df, signal.shift(1).fillna(0), b, sc)["strat_ret"])["夏普比率"]
    print(f"穩健性：成本加倍夏普 {double:.2f}，延遲一天夏普 {delay:.2f}")

    beta = np.polyfit(bh, res["strat_ret"], 1)[0]
    up, down = bh > 0, bh < 0
    print(f"擇時：Beta {beta:.2f}，上漲捕獲 {res['strat_ret'][up].mean() / bh[up].mean():.0%}，"
          f"下跌捕獲 {res['strat_ret'][down].mean() / bh[down].mean():.0%}")
    return res


if __name__ == "__main__":
    data = load_prices(DATA_FILE)
    for name, func in STRATEGIES.items():
        evaluate(data, name, func)
