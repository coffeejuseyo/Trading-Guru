"""產生模擬交易練習器 index.html：把課程資料 sample_long.csv 內嵌進 template.html。

用法（在 repo 根目錄）：
    python tools/trading-simulator/build.py

產生的 index.html 不需要網路與伺服器，直接用瀏覽器打開即可。
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "lessons" / "phase-10" / "data" / "sample_long.csv"


def compact_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = r["Date"].replace("-", "")
            vals = [float(r[k]) for k in ("Open", "High", "Low", "Close")]
            rows.append(",".join([d] + [f"{v:g}" for v in vals] + [str(int(float(r["Volume"])))]))
    return ";".join(rows)


def main():
    data = compact_rows(DATA)
    html = (HERE / "template.html").read_text(encoding="utf-8")
    assert '"__DATA__"' in html
    out = html.replace('"__DATA__"', '"' + data + '"')
    (HERE / "index.html").write_text(out, encoding="utf-8")
    print(f"index.html：{len(out) / 1024:.0f} KB，{data.count(';') + 1} 根 K 線")


if __name__ == "__main__":
    main()
