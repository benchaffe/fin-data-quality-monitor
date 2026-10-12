import json
import os
import time
from pathlib import Path
import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()
HEADERS = {"User-Agent": os.environ["SEC_USER_AGENT"]}
RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

TICKERS = [
    "AAPL", "MSFT", "GOOGL", "NVDA", "ORCL", "INTC",
    "JPM", "BAC", "GS", "MS", "WFC", "C",
    "JNJ", "PFE", "UNH", "MRK", "ABBV",
    "WMT", "KO", "PG", "XOM", "CVX", "HD", "MCD", "COST",
]

@retry(stop=stop_after_attempt(4), wait=wait_exponential(min=1, max=20))
def get_json(url: str) -> dict:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

def main() -> None:
    mapping = get_json("https://www.sec.gov/files/company_tickers.json")
    cik_by_ticker = {v["ticker"]: str(v["cik_str"]).zfill(10) for v in mapping.values()}
    for ticker in TICKERS:
        cik = cik_by_ticker.get(ticker)
        if cik is None:
            print(f"No CIK found for {ticker}")
            continue
        out = RAW / f"CIK{cik}.json"
        if out.exists():
            continue
        out.write_text(json.dumps(get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")))
        print(f"Saved {ticker} -> {out.name}")
        time.sleep(0.2)

if __name__ == "__main__":
    main()
