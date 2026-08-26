"""
Loads raw OHLCV CSVs for a specific universe calculating the returns, volatility, etc,
checks the data, then saves a processed Dataframe.
"""

import os
import sys
import pandas as pd 
import numpy as np

sys.path.append (os.path.join (os.path.dirname(__file__), "..", ".."))
from src.config import UNIVERSES, RAW_DATA_DIR, PROCESSED_DATA_DIR

def load_raw_prices (universe_name: str) -> dict: 
    """ Load raw ticker CSVs into a dictionary"""
    tickers = UNIVERSES[universe_name]["tickers"]
    raw_dir = os.path.join(RAW_DATA_DIR, universe_name)

    price_data = {}
    for ticker in tickers: 
        path = os.path.join(raw_dir, f"{ticker}.csv")
        if not os.path.exists(path):
            print (f" WARNING: {path} not found, skipping {ticker}.")
            continue
        df = pd.read_csv(path, index_col=0, parse_dates=True)
        price_data[ticker] = df
    
    return price_data 

def sanity_check (ticker: str, df: pd.DataFrame):
    """ Data Quality Warnings"""
    issues = []

    if df["Close"].isna().sum() > 0:
        issues.apppend(f"{df['Close'].isna().sum()} NaN values in Close")
    if (df["Close"] <= 0).sum() > 0:
        issues.append (f"{(df['Close'] <= 0) .sum()}) non-positive Close prices")

    """ Gap check: Flag any gap surpassing 10 calender days """
    date_diffs = df.index.to_series().diff().dt.days
    big_gaps = date_diffs[date_diffs > 10]
    if len(big_gaps) > 0:
        issues.append(f"{len(big_gaps)} gaps > 10 days (possible missing data)")

    if issues:
        print(f"  [{ticker}] Issues found: {'; '.join(issues)}")
    else:
        print(f"  [{ticker}] OK — {len(df)} rows, {df.index.min().date()} to {df.index.max().date()}")

def engineer_features (ticker: str, df: pd.DataFrame) -> pd.DataFrame: 
    """ compute returns, rolling volatility & momentum for one asset"""
    out = pd.DataFrame (index = df.index)

    out [f"{ticker}_close"] = df["Close"]
    out [f"{ticker}_return"] = df["Close"].pct_change()
    out [f"{ticker}_vol_21d"] = out [f"{ticker}_return"].rolling(21).std()
    out [f"{ticker}_momentum_21d"] = df["Close"].pct_change(21)
    out [f"{ticker}_momentum_63d"] = df["Close"].pct_change(63)

    return out 

def prepreprocess_universe(universe_name: str):
    print (f"\n Processing universe: {universe_name}")
    price_data = load_raw_prices(universe_name)

    feature_frames = []
    for ticker, df in price_data.items():
        sanity_check (ticker,df)
        feature_frames.append(engineer_features(ticker,df))

    """ Aligning all ticker on shared dats & rows """
    combined = pd.concat (feature_frames, axis = 1).dropna()
    
    out_dir = os.path.join (PROCESSED_DATA_DIR, universe_name)
    os.makedirs(out_dir, exist_ok = True)
    out_path = os.path.join (out_dir, "features.csv")
    combined.to_csv(out_path)

    print (f" Saved combined feature set: {combined.shape[0]} rows x {combined.shape[1]} cols -> {out_path}")

    if __name__ == "__main__": 
        for universe_name in UNIVERSES:
            prepreprocess_universe(universe_name)
