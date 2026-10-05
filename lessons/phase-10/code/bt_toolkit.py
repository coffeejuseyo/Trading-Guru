"""
Phase 10 回測工具箱（教學用）
================================
把 Phase 9～10 寫過的函式整理在一起，方便之後的單元重複使用：

    from bt_toolkit import load_prices, sma, rsi, atr, state_signal, backtest, \
        tw_costs, perf_stats, extract_trades, trade_stats, report

約定（和 8.1、8.13 的規格書一致）：
- signal：在第 t 天「收盤後」才知道的目標部位（1 = 持有、0 = 空手）
- 執行：第 t+1 天「開盤價」成交
- 成本：買進、賣出各自的成本比例（例如 0.000855 = 0.0855%）

⚠️ 這是教學用的簡化工具：只做多、全額進出、不考慮漲跌停與流動性。
"""
import numpy as np
import pandas as pd


# ---------------------------------------------------------------- 資料與指標
def load_prices(path):
    """讀入 Date, Open, High, Low, Close, Volume 格式的 CSV。"""
    return pd.read_csv(path, parse_dates=["Date"], index_col="Date")


def sma(series, n):
    return series.rolling(n).mean()


def ema(series, n):
    return series.ewm(span=n, adjust=False).mean()


def rsi(close, n=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    avg_loss = loss.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + avg_gain / avg_loss)


def atr(df, n=14):
    prev_close = df["Close"].shift(1)
    tr = pd.concat([df["High"] - df["Low"],
                    (df["High"] - prev_close).abs(),
                    (df["Low"] - prev_close).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def state_signal(entry, exit, max_days=None):
    """把「進場條件」與「出場條件」轉成持有狀態（1 / 0）。

    entry、exit：每天收盤後判斷的 True / False（例如 RSI(2) < 10、收盤 > 5 日均線）。
    max_days：持有滿幾天就出場（時間停損），None 表示不限。
    進場當天訊號即為 1；從隔天起才檢查出場條件。
    """
    index = entry.index
    entry = entry.fillna(False).astype(bool).values
    exit = exit.fillna(False).astype(bool).values
    sig = np.zeros(len(entry))
    holding, days = False, 0
    for i in range(len(entry)):
        if holding:
            days += 1
            if exit[i] or (max_days is not None and days >= max_days):
                holding = False
        elif entry[i]:
            holding, days = True, 0
        sig[i] = 1.0 if holding else 0.0
    return pd.Series(sig, index=index)


# ---------------------------------------------------------------- 成本
def tw_costs(fee_rate=0.001425, discount=0.6, tax_rate=0.003, slippage=0.0):
    """回傳（買進成本比例, 賣出成本比例）。
    台股預設：手續費 0.1425% × 折扣、賣出交易稅 0.3%（ETF 常見為 0.1%），
    slippage 為每次成交不利的比例。費率以券商與政府最新規定為準。"""
    fee = fee_rate * discount
    return fee + slippage, fee + tax_rate + slippage


# ---------------------------------------------------------------- 向量化回測
def backtest(df, signal, buy_cost=0.0, sell_cost=0.0):
    """向量化回測（只做多）。

    signal：第 t 天收盤後決定的目標部位（0～1）。
    第 t+1 天開盤成交，因此第 t 天實際持有的部位 pos = signal.shift(1)。
    每天拆成兩段：隔夜（昨收→今開，持有昨天的部位）、日內（今開→今收，持有今天的部位）。
    """
    signal = signal.fillna(0)
    pos = signal.shift(1).fillna(0)          # 今天開盤後持有的部位
    prev_pos = pos.shift(1).fillna(0)        # 昨天收盤時持有的部位
    r_night = (df["Open"] / df["Close"].shift(1) - 1).fillna(0)
    r_day = df["Close"] / df["Open"] - 1
    change = pos - prev_pos
    cost = np.where(change > 0, buy_cost, sell_cost) * change.abs()
    strat_ret = (1 + prev_pos * r_night) * (1 - cost) * (1 + pos * r_day) - 1

    out = pd.DataFrame(index=df.index)
    out["signal"] = signal
    out["pos"] = pos
    out["strat_ret"] = strat_ret
    out["equity"] = (1 + strat_ret).cumprod()
    out["bh_equity"] = df["Close"] / df["Close"].iloc[0]
    return out


# ---------------------------------------------------------------- 績效指標
def max_drawdown_duration(equity):
    """最長回撤期間（日曆天數）：從前高到重新創新高（或資料結束）的最長時間。"""
    peak = equity.cummax()
    longest, start = pd.Timedelta(0), None
    for date, (v, p) in zip(equity.index, zip(equity.values, peak.values)):
        if v < p:
            if start is None:
                start = prev_date
        elif start is not None:
            longest = max(longest, date - start)
            start = None
        prev_date = date
    if start is not None:
        longest = max(longest, equity.index[-1] - start)
    return longest.days


def perf_stats(ret, periods=252, rf=0.0):
    """由每日報酬計算績效指標。rf 為年化無風險利率。"""
    ret = ret.fillna(0)
    equity = (1 + ret).cumprod()
    years = (ret.index[-1] - ret.index[0]).days / 365.25
    total = equity.iloc[-1] - 1
    cagr = (1 + total) ** (1 / years) - 1
    vol = ret.std() * np.sqrt(periods)
    excess = ret - rf / periods
    sharpe = excess.mean() / ret.std() * np.sqrt(periods) if ret.std() > 0 else np.nan
    downside = np.sqrt((np.minimum(excess, 0) ** 2).mean()) * np.sqrt(periods)
    sortino = excess.mean() * periods / downside if downside > 0 else np.nan
    mdd = (equity / equity.cummax() - 1).min()
    calmar = cagr / abs(mdd) if mdd < 0 else np.nan
    return {
        "總報酬": total,
        "年化報酬": cagr,
        "年化波動": vol,
        "最大回撤": mdd,
        "夏普比率": sharpe,
        "Sortino": sortino,
        "Calmar": calmar,
        "最長回撤天數": max_drawdown_duration(equity),
    }


# ---------------------------------------------------------------- 交易紀錄與統計
def extract_trades(df, res):
    """從回測結果找出每一筆交易（第 t 天開盤進場、第 u 天開盤出場）。
    報酬率用持有期間每日的策略報酬連乘，因此已包含成本。"""
    pos = res["pos"]
    prev = pos.shift(1).fillna(0)
    entries = list(res.index[(pos > 0) & (prev == 0)])
    exits = list(res.index[(pos == 0) & (prev > 0)])
    trades = []
    for entry in entries:
        later_exits = [x for x in exits if x > entry]
        exit_ = later_exits[0] if later_exits else res.index[-1]
        is_open = not later_exits
        r = (1 + res.loc[entry:exit_, "strat_ret"]).prod() - 1
        trades.append({
            "entry_date": entry,
            "exit_date": exit_,
            "entry_price": df.loc[entry, "Open"],
            "exit_price": df.loc[exit_, "Close"] if is_open else df.loc[exit_, "Open"],
            "return": r,
            "days": (exit_ - entry).days,
            "open": is_open,
        })
    return pd.DataFrame(trades)


def trade_stats(trades):
    """交易統計（只計算已平倉的交易）。"""
    t = trades[~trades["open"]] if "open" in trades else trades
    r = t["return"]
    wins, losses = r[r > 0], r[r <= 0]
    streak = max_streak = 0
    for x in r:
        streak = streak + 1 if x <= 0 else 0
        max_streak = max(max_streak, streak)
    avg_win = wins.mean() if len(wins) else 0.0
    avg_loss = losses.mean() if len(losses) else 0.0
    return {
        "交易次數": len(r),
        "勝率": len(wins) / len(r) if len(r) else np.nan,
        "平均獲利": avg_win,
        "平均虧損": avg_loss,
        "盈虧比": avg_win / abs(avg_loss) if avg_loss < 0 else np.nan,
        "獲利因子": wins.sum() / abs(losses.sum()) if losses.sum() < 0 else np.nan,
        "每筆期望值": r.mean() if len(r) else np.nan,
        "最大連虧": max_streak,
        "平均持有天數": t["days"].mean() if len(t) else np.nan,
    }


# ---------------------------------------------------------------- 報告
def _fmt(k, v):
    if isinstance(v, (int, np.integer)) or k in ("交易次數", "最大連虧", "最長回撤天數"):
        return f"{v:,.0f}"
    if k in ("夏普比率", "Sortino", "Calmar", "盈虧比", "獲利因子", "平均持有天數"):
        return f"{v:.2f}"
    return f"{v:.2%}"


def report(df, res, title="策略"):
    """印出策略與買進持有的績效對照，以及交易統計。"""
    s = perf_stats(res["strat_ret"])
    b = perf_stats(df["Close"].pct_change())
    print(f"{'指標':<8}{title:>12}{'買進持有':>12}")
    for k in s:
        print(f"{k:<8}{_fmt(k, s[k]):>12}{_fmt(k, b[k]):>12}")
    print(f"{'市場曝險':<8}{res['pos'].mean():>12.1%}{1:>12.0%}")
    print("-" * 34)
    for k, v in trade_stats(extract_trades(df, res)).items():
        print(f"{k:<8}{_fmt(k, v):>12}")
