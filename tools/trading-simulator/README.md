# 🕹️ K 線駕訓班：模擬交易練習器

逐根播放 K 線的模擬交易練習器，搭配 [模擬交易路線圖](../../docs/SIMULATION.md) 的第 1～5 關使用。

## 怎麼打開

1. 下載整個 repo（GitHub 頁面上的「Code → Download ZIP」，或 `git clone`）。
2. 用瀏覽器（Chrome、Edge、Safari、Firefox）直接打開 `tools/trading-simulator/index.html`。
3. 不需要安裝任何東西，也不需要網路（有網路時字型會比較好看）。

> GitHub 網頁本身不會執行 HTML，所以要下載後在自己的電腦打開。

## 怎麼練習

| 步驟 | 做什麼 |
|---|---|
| ① | 看目前的 K 線圖（只看得到「今天」以前，未來的 K 線看不到） |
| ② | 想進場：在右邊設好**停損價**、選**每筆風險**、寫下**理由**、選**情緒分數**，按「送出：明天開盤買進」 |
| ③ | 按「下一根 K 線」（或鍵盤 <kbd>N</kbd>、<kbd>→</kbd>）：委託在下一根的**開盤**成交；盤中碰到停損就自動出場 |
| ④ | 持有中可以把停損**往上**移（移動停損）；往下移會被記為「放寬停損」違規 |
| ⑤ | 出場後填寫檢討：有沒有遵守規則、違規類型、照規則會是幾 R |
| ⑥ | 看成績單與關卡進度；在「交易日誌」匯出 CSV |

## 成交規則（和 Phase 10 的回測一致）

- 收盤後做決定，**下一根 K 線開盤**成交（8.1、10.2）。
- 盤中最低價碰到停損就出場；開盤就跳空跌破停損時，以**開盤價**出場（10.3）。
- 成本：手續費 0.1425% × 6 折（買賣各一次）、賣出交易稅 0.3%、每次成交滑價 0.05%。
- **R 倍數** = 這筆的淨損益（含成本）÷ 進場時的風險金額（股數 × 每股風險）。
- 股數 = 帳戶資產 × 每筆風險 ÷（收盤價 − 停損價），無條件捨去（6.4）。
- 只做多。

## 匯出的 CSV

欄位和 [Phase 12 的練習日誌](../../lessons/phase-12/data/paper_journal.csv)完全相同：

```
trade_id,entry_date,exit_date,symbol,strategy,signal_price,fill_price,stop_price,exit_price,R,R_if_rules,followed_rules,violation,emotion
```

所以可以直接用 [12.3](../../lessons/phase-12/12.3-weekly-review.md)、[12.4](../../lessons/phase-12/12.4-live-vs-backtest.md) 的程式分析：把 `pd.read_csv("paper_journal.csv")` 換成你存的檔名即可。

## 練習資料

- **課程資料**：內嵌 [`lessons/phase-10/data/sample_long.csv`](../../lessons/phase-10/data/sample_long.csv)，每次從隨機位置開始，最多播放 500 根。
- **隨機產生新走勢**：每次產生一段新的模擬價格（有多頭、空頭、盤整與波動群聚）。

> ⚠️ 兩種資料都是亂數產生的模擬價格，不代表任何真實商品，也不構成投資建議。真實行情的練習請用 TradingView 模擬交易或券商模擬平台。

## 紀錄會保存嗎？

練習進度與日誌存在**瀏覽器的本機儲存空間**：同一台電腦、同一個瀏覽器重新打開會接著練。換瀏覽器、使用無痕視窗或清除網站資料就會消失，所以**每練完一段就匯出 CSV 存檔**。

## 給維護者

`index.html` 由 `build.py` 產生（把 `template.html` 與課程資料合併成單一檔案）。修改畫面或邏輯時改 `template.html`，再執行：

```
python tools/trading-simulator/build.py
```
