"""
Historical data pulling OHLCV data from yfinance for a given universe
saves raw CSVs to raw/{universe_name}
"""

import os
import sys
import yfinance as yf

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from src.config import UNIVERSES, START_DATE, END_DATE, RAW_DATA_DIR


def fetch_universe(universe_name: str):
    if universe_name not in UNIVERSES:
        raise ValueError(f"Unknown universe '{universe_name}'. Options: {list(UNIVERSES.keys())}")

    tickers = UNIVERSES[universe_name]["tickers"]
    out_dir = os.path.join(RAW_DATA_DIR, universe_name)
    os.makedirs(out_dir, exist_ok=True)

    print(f"Fetching {len(tickers)} tickers for '{universe_name}': {tickers}")

    for ticker in tickers:
        print(f"  Downloading {ticker}...")
        df = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)

        if df.empty:
            print(f"  WARNING: no data returned for {ticker}, skipping.")
            continue

        out_path = os.path.join(out_dir, f"{ticker}.csv")
        df.to_csv(out_path)
        print(f"  Saved {len(df)} rows to {out_path}")

    print(f"Done fetching '{universe_name}'.\n")


if __name__ == "__main__":
    for universe_name in UNIVERSES:
        fetch_universe(universe_name)