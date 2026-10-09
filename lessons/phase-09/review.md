# Phase 9｜總複習與實作作業

> ⏱️ 約 4–6 小時（含 0050 / SPY 分析作業）｜[← Phase 9 目錄](README.md)｜[下一階段：Phase 10 時光機實驗室：回測 →](../phase-10/README.md)

> 📌 **作答方式**：Part A、B 先**不看講義、不執行程式**，在紙上寫下答案，再打開答案對照；最後可以執行程式驗證。
> 🎯 **通過標準**：Part A + B 答對 80% 以上、Part C 兩題都能順利講完、Part D 作業完成並通過驗收清單。

---

## 🗺️ Phase 9 觀念地圖

```
            【電腦 = 超聽話、不會變通的機器人；Python = 跟它溝通的語言】
                                   │
  基本功（9.1～9.6）
    收納盒（變數、型別）→ 下雨帶傘（if）→ 洗碗（for / while）
    → 按鈕（函式 + assert 測試）→ 購物清單與電話簿（串列、字典）
                                   │
  資料工具（9.7～9.9）
    NumPy 整排計算（向量化、√252、cummax 回撤、蒙地卡羅）
    pandas 超強 Excel（loc / iloc、pct_change、⭐ shift、篩選、groupby）
    時間序列（resample 週月線、rolling 均線與波動、過去 N 日要 shift(1)）
                                   │
  金融資料實戰（9.10～9.13）
    採買（yfinance、CSV、API、存本機、檢查清單）
    → 洗菜（缺值不用 bfill、⭐ 除權息與分割調整）
    → 上菜（畫圖抓 bug、K 線、買賣點）
    → 自己下廚（SMA、RSI、ATR、布林、MACD、KD，手算驗證、和 TradingView 比對）
                                   │
  工作習慣（9.14）：遊戲存檔（Git、.gitignore 保護金鑰）
                                   ▼
                      Phase 10：把規格書交給電腦回測
```

---

## Part A｜選擇題（每題 1 分，共 10 分）

**1.** 執行 `print(17 // 5, 17 % 5)` 的結果是：
- (A) `3.4 2`
- (B) `3 2`
- (C) `3 3`
- (D) `4 2`

**2.** `0.1 + 0.2 == 0.3` 的結果是 `False`，原因是：
- (A) Python 的加法有 bug
- (B) 浮點數以二進位儲存，有微小誤差
- (C) 要用 `=` 才能比較
- (D) 0.3 不是數字

**3.** `prices = [50, 51, 52, 53, 54]`，`prices[-3:]` 的結果是：
- (A) `[50, 51, 52]`
- (B) `[52, 53, 54]`
- (C) `[53, 54]`
- (D) `[51, 52, 53]`

**4.** 日報酬標準差 1%，年化波動約為：
- (A) 1%
- (B) 2.52%
- (C) 15.9%
- (D) 252%

**5.** 在 pandas 中，要讓每一列看到「前一天」的收盤價，應該用：
- (A) `df["Close"].shift(1)`
- (B) `df["Close"].shift(-1)`
- (C) `df["Close"].diff()`
- (D) `df["Close"].rolling(1)`

**6.** 突破規則「收盤價 > 過去 20 日最高收盤價」的正確寫法是：
- (A) `df["Close"] > df["Close"].rolling(20).max()`
- (B) `df["Close"] > df["Close"].rolling(20).max().shift(1)`
- (C) `df["Close"] > df["Close"].rolling(20).max().shift(-1)`
- (D) `df["Close"] > df["Close"].max()`

**7.** 把日 K 重取樣成週 K 時，Volume 應該用：
- (A) `first`
- (B) `last`
- (C) `mean`
- (D) `sum`

**8.** 回測中填補缺值，**不應該**使用：
- (A) `ffill()`
- (B) `dropna()`
- (C) `bfill()`
- (D) 先檢查原因再決定

**9.** 某 ETF 收盤 102 元，隔天除息 2 元、收盤 100 元。含股利的真實報酬約為：
- (A) −1.96%
- (B) 0%
- (C) +1.96%
- (D) −2%

**10.** 以下哪一個檔案**最不應該**被 commit 進 Git 並上傳到 GitHub？
- (A) `indicators.py`
- (B) `README.md`
- (C) 存有 API 金鑰的 `.env`
- (D) 策略規格書

---

## Part B｜是非題（每題 1 分，共 10 分）

**11.** 在 Python 中，`=` 是比較兩個值是否相等。（○ / ✕）

**12.** `range(1, 5)` 會產生 1、2、3、4、5。（○ / ✕）

**13.** 函式中用 `print` 顯示結果，和用 `return` 回傳結果，效果相同。（○ / ✕）

**14.** 累積報酬應該用 (1 + 日報酬) 連乘再減 1，而不是把日報酬相加。（○ / ✕）

**15.** `df.loc["2022-03-01":"2022-03-04"]` 包含 3 月 4 日。（○ / ✕）

**16.** pandas 的條件篩選可以寫成 `df[df["A"] > 1 and df["B"] > 2]`。（○ / ✕）

**17.** rolling(20) 的視窗預設包含今天。（○ / ✕）

**18.** 股票 1 拆 4 的當天，原始價格的單日報酬約 −75%，這代表持有人虧損 75%。（○ / ✕）

**19.** 自己寫的 RSI 和 TradingView 在資料前段有些微差異，一定是程式寫錯。（○ / ✕）

**20.** 黃金交叉的判斷，需要同時比較今天與昨天的均線位置。（○ / ✕）

---

## Part C｜費曼口說題（錄音作答，各 1 分鐘）

> 回想 [費曼檢核表](../../templates/feynman-check.md)：有比喻、有數字、有常見誤解。

**21.** 為什麼交易者要學寫程式？用「機器人照食譜做菜」說明。

**22.** 什麼是「除權息調整」？為什麼不調整會讓回測出錯？

---

## Part D｜課綱作業：0050 / SPY 完整分析

用 Python 完成以下作業（在 Colab 或 Jupyter 中，一個筆記本完成）：

| # | 任務 | 對應單元 |
|---|---|---|
| 1 | 下載 0050.TW（或 SPY）**10 年**日線資料，`auto_adjust=False`，存成 CSV | 9.10 |
| 2 | 執行資料檢查清單；找出所有「原始收盤價單日跌超過 4%，但還原收盤價跌不到 1%」的日子並查證原因 | 9.10、9.11 |
| 3 | 用**還原價格**計算：每日報酬、**總報酬、年化報酬、年化波動、最大回撤**（含谷底與前高日期） | 9.7～9.9 |
| 4 | 比較用原始價格與還原價格算出的年化報酬，差多少？ | 9.11 |
| 5 | 做出**年度報酬表**與**月報酬表** | 9.9 |
| 6 | **自己寫函式**計算 20 日均線、14 日 RSI，挑最近 5 天和 TradingView 比對並填表 | 9.13 |
| 7 | 畫出「價格 + 20 / 60 日均線 + 成交量」圖、「資金曲線 + 回撤」圖 | 9.12 |
| 8 | 把筆記本與 `indicators.py` 用 Git 存檔（或存到 GitHub 私人儲存庫） | 9.14 |

**最後，用文字回答（每題 3～5 句）：**
1. 這 10 年的年化報酬、年化波動、最大回撤各是多少？如果你在最大回撤開始前買進，要等多久才回到前高？
2. 原始價格與還原價格的報酬差距有多大？如果用原始價格回測，會得出什麼錯誤的結論？
3. 你的 SMA20、RSI14 和 TradingView 一致嗎？若有差異，原因是什麼？
4. 這個「買進持有」的結果，就是 Phase 10 所有策略的**對照基準**（8.11）。你覺得你的策略要比它好在哪裡，才值得花時間執行？

### 參考程式（用練習資料示範，換成你的資料即可）

<details><summary>展開參考程式</summary>

以下程式用 [`data/sample_prices.csv`](data/sample_prices.csv) 示範第 3、5、6、7 項。換成真實資料時，把讀檔的部分改成 9.10 的 `load_prices()`，並把 `PRICE` 改成還原價格欄位（`"Adj Close"`）。

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===== 1. 讀取資料 =====
df = pd.read_csv("sample_prices.csv", parse_dates=["Date"], index_col="Date")
PRICE = "Close"        # 真實資料請改成 "Adj Close"（還原價格）

# ===== 2. 指標函式（9.13）=====
def sma(series, n):
    return series.rolling(n).mean()

def rsi(close, n=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    avg_loss = loss.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + avg_gain / avg_loss)

# ===== 3. 績效摘要（9.7～9.9）=====
def performance(price):
    ret = price.pct_change().dropna()
    total = price.iloc[-1] / price.iloc[0] - 1
    years = (price.index[-1] - price.index[0]).days / 365.25
    cagr = (1 + total) ** (1 / years) - 1
    vol = ret.std() * np.sqrt(252)
    dd = price / price.cummax() - 1
    trough = dd.idxmin()
    peak_date = price[:trough].idxmax()
    recovered = price[trough:][price[trough:] >= price[peak_date]]
    recovery_date = recovered.index[0] if len(recovered) > 0 else None
    return {
        "總報酬": f"{total:.2%}",
        "年化報酬": f"{cagr:.2%}",
        "年化波動": f"{vol:.2%}",
        "最大回撤": f"{dd.min():.2%}",
        "前高日期": peak_date.date(),
        "谷底日期": trough.date(),
        "回到前高": recovery_date.date() if recovery_date is not None else "尚未回到前高",
    }

for k, v in performance(df[PRICE]).items():
    print(f"{k}：{v}")

# ===== 4. 年度與月報酬表 =====
year_end = df[PRICE].resample("YE").last()
yearly = year_end.pct_change()
yearly.iloc[0] = year_end.iloc[0] / df[PRICE].iloc[0] - 1     # 第一年：從資料第一天算起
yearly.index = yearly.index.year
print((yearly * 100).round(2))

month_end = df[PRICE].resample("ME").last()
m = month_end.pct_change().to_frame("ret")
m["year"], m["month"] = m.index.year, m.index.month
print((m.pivot(index="year", columns="month", values="ret") * 100).round(1))

# ===== 5. 指標與比對用表格 =====
df["SMA20"] = sma(df[PRICE], 20)
df["SMA60"] = sma(df[PRICE], 60)
df["RSI14"] = rsi(df[PRICE], 14)
print(df[[PRICE, "SMA20", "RSI14"]].tail(5).round(2))

# ===== 6. 圖表（9.12）=====
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True,
                               gridspec_kw={"height_ratios": [3, 1]})
ax1.plot(df.index, df[PRICE], label="Price", linewidth=1)
ax1.plot(df.index, df["SMA20"], label="SMA20", linewidth=1)
ax1.plot(df.index, df["SMA60"], label="SMA60", linewidth=1)
ax1.legend()
ax1.grid(alpha=0.3)
ax2.bar(df.index, df["Volume"], width=1.0)
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("homework_price_volume.png", dpi=120)

growth = df[PRICE] / df[PRICE].iloc[0]
dd = df[PRICE] / df[PRICE].cummax() - 1
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True,
                               gridspec_kw={"height_ratios": [2, 1]})
ax1.plot(growth.index, growth, linewidth=1)
ax1.set_title("Buy and Hold")
ax1.grid(alpha=0.3)
ax2.fill_between(dd.index, dd, 0, color="tab:red", alpha=0.4)
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("homework_equity_drawdown.png", dpi=120)
plt.show()
```

用練習資料執行的績效摘要：

```
總報酬：25.37%
年化報酬：7.88%
年化波動：19.20%
最大回撤：-24.66%
前高日期：2022-03-04
谷底日期：2022-06-20
回到前高：2022-10-17
```

> 💡 這裡的年化報酬（7.88%）用**日曆天數**計算，9.9 用 252 個交易日計算得到 7.59%。差異來自模擬資料沒有扣除國定假日，一年有約 260 個「交易日」；真實資料兩種算法會更接近。報告中寫清楚你用哪一種即可。

</details>

### Part D 驗收清單

- [ ] 資料存成 CSV，並記錄來源、下載日期、是否還原權值
- [ ] 資料檢查清單全部執行，異常日期已查證原因
- [ ] 算出總報酬、年化報酬、年化波動、最大回撤（含前高、谷底、回到前高的日期）
- [ ] 比較原始與還原價格的報酬差異
- [ ] 完成年度報酬表與月報酬表
- [ ] 自己寫的 SMA20、RSI14 與 TradingView 比對表（5 天）
- [ ] 兩張圖：價格 + 均線 + 成交量、資金曲線 + 回撤
- [ ] 用 Git 存檔，`.gitignore` 排除資料檔與金鑰
- [ ] 回答 4 個問題

---

## 📝 答案

<details><summary>Part A 選擇題答案</summary>

1. **(B)**：`//` 整數除法得 3，`%` 餘數得 2（9.2）。
2. **(B)**：浮點數的二進位表示誤差（9.2）。
3. **(B)**：負索引從後面數，`[-3:]` 是最後 3 個（9.6）。
4. **(C)**：1% × √252 ≈ 15.9%（9.7）。
5. **(A)**：`shift(1)` 是前一天；`shift(-1)` 是明天，會造成前視偏差（9.8）。
6. **(B)**：「過去」20 日不含今天，要 `shift(1)`；(A) 永遠不成立，(C) 偷看未來，(D) 用了全期間（未來）的最高價（9.9）。
7. **(D)**：成交量加總（9.9）。
8. **(C)**：bfill 用未來的值填補，造成前視偏差（9.11）。
9. **(B)**：(100 + 2) ÷ 102 − 1 = 0%（9.11）。
10. **(C)**：金鑰上傳後可能被盜用（9.14）。

</details>

<details><summary>Part B 是非題答案</summary>

11. **✕**：`=` 是指派，`==` 才是比較。
12. **✕**：不包含 5，只有 1～4。
13. **✕**：print 只顯示；return 才能把結果交給呼叫者使用。
14. **○**
15. **○**：`loc` 的標籤切片頭尾都包含。
16. **✕**：要寫 `df[(df["A"] > 1) & (df["B"] > 2)]`。
17. **○**
18. **✕**：股數變成 4 倍，總市值不變；需要分割調整。
19. **✕**：遞迴指標的起始值與資料長度不同，會造成前段差異；應比對後段數值。
20. **○**

</details>

<details><summary>Part C 費曼口說題參考要點</summary>

**21.** 電腦像一個超聽話、速度超快、永遠不累、但完全不會變通的機器人廚師：你說「加一點鹽」它會問幾克，寫錯一個字它就停下來。交易者學寫程式，是因為手動目測回測太慢（30 筆要好幾小時）、容易看錯算錯、樣本太少、還會不自覺挑好看的交易；寫成程式後，十年資料、上千筆交易幾秒鐘算完，規則改一個數字就能重跑。而機器人不會變通這個特性，正好逼你把規則寫得像 8.13 的規格書一樣明確。常見誤解：不用把 Python 學到精通，會 pandas 的基本操作就能開始回測。

**22.** 除息時股價會扣掉股利（例如收盤 102、配息 2 元、隔天參考價 100），看起來跌了約 2%，但持有人拿到 2 元現金，總報酬是 0。除權息調整（還原價格）是把除息日之前的價格依比例往下調整，讓價格變化只反映真實漲跌。不調整的話：回測會把每次除息當成虧損，長期報酬被嚴重低估（配息 3%～4% 的 ETF，十年差距很大）；除息的跳空還可能觸發停損或進場訊號，產生假交易。分割更嚴重：1 拆 4 的那天，原始價格看起來暴跌 75%。原則：報酬與訊號用還原價格，實際下單股數用原始價格。

</details>

---

## ✅ Phase 9 完成檢查

- [ ] Part A + B 答對 16 題以上（80%）
- [ ] Part C 兩題都錄音完成，自評有比喻、有數字、有誤解
- [ ] 各單元練習完成，特別是 9.5（函式測試）、9.8（找 bug）、9.13（手算指標）
- [ ] 建立指標函式庫 `indicators.py`（[9.13 練習 4](9.13-indicators-in-pandas.md)）
- [ ] 建立研究儲存庫並用 Git 存檔（[9.14](9.14-git-basics.md)）
- [ ] **Part D：0050 / SPY 完整分析，驗收清單全部打勾**
- [ ] 到 [PROGRESS.md](../../docs/PROGRESS.md) 把 Phase 9 打勾 🎉

**恭喜完成 Phase 9！** 🎉

幾週前，你可能連 Python 是什麼都不知道。現在你已經可以：下載十年的股價、清理資料、處理除權息、計算績效與指標、畫出專業的圖表，還會用 Git 管理你的研究。

更重要的是，你養成了三個回測研究者最重要的習慣：**用小例子手算驗證**、**畫圖檢查**、**永遠不偷看未來（shift(1)）**。

下一站：**Phase 10 時光機實驗室：回測**——本課程的重點。你會把 Phase 8 的 3 份策略規格書交給電腦，在十年的資料上嚴格地回測，加入交易成本，學會辨認前視偏差、過度擬合、倖存者偏差這些「回測陷阱」，並寫出你的第一份正式回測報告。
