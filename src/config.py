""" 
Central Configuration for all universes
Fetch, Processes, Trains, Evals, etc, will or should at least be imported from this file.
"""

UNIVERSES =  {
"sector_etfs": {
    "tickers": ["XLK", "XLF", "XLV", "XLY", "XLP", "XLI"],
    "description": "Sector rotation across SPDR sector ETFs",
},
"large_cap_stocks": {
"tickers": ["AAPL", "MSFT", "JPM", "JNJ", "XOM", "PG", "CAT", "AMZN"],
"description": "Individual large-cap stocks",
},
"broad_market": {
    "tickers": ["SPY", "QQQ", "TLT", "GLD", "IWM"],
    "description": "Cross-asset class allocation (Equities, Bonds, Etc.)"
}
}

# Shared date ranges
START_DATE = "2015-01-01"
TRAIN_END_DATE = "2019-12-31"
TEST_START_DATE= "2020-01-01"
END_DATE = "2026-12-31"

# Paths
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
RESULTS_DIR = "data/results"