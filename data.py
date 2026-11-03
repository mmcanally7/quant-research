import os

import pandas as pd
import yfinance as yf


def load_prices(tickers, start, end, cache_dir="data_cache", refresh=False):
    """
    Download daily adjusted closing prices from Yahoo Finance, with a local cache.

    tickers: a ticker string ("SPY") or a list of tickers (["SPY", "QQQ"]).
    start, end: dates as "YYYY-MM-DD" strings.
    cache_dir: folder for cached CSV files, one per ticker and date range.
    refresh: if True, download again even when a cached file exists.
    Returns: DataFrame indexed by date, one column per ticker.
             Tickers with no data are dropped with a warning.

    Note: Yahoo has no history for delisted companies, so results
    for a list of today's stocks carry survivorship bias.
    """
    # Accept a single ticker as well as a list
    if isinstance(tickers, str):
        tickers = [tickers]

    os.makedirs(cache_dir, exist_ok=True)
    frames = []

    for ticker in tickers:
        path = os.path.join(cache_dir, f"{ticker}_{start}_{end}.csv")

        if os.path.exists(path) and not refresh:
            series = pd.read_csv(path, index_col=0, parse_dates=True).iloc[:, 0]
        else:
            series = yf.download(ticker, start=start, end=end, auto_adjust=True)["Close"].iloc[:, 0]
            # Skip caching failed downloads, so a typo isn't saved as an empty file
            if not series.empty:
                series.to_csv(path)

        frames.append(series)

    # Combine tickers, aligning them by date
    prices = pd.concat(frames, axis=1)
    prices.columns = tickers

    # Drop tickers that returned no data
    empty = [t for t in tickers if prices[t].isna().all()]
    for ticker in empty:
        print(f"{ticker}: no data from yfinance (misspelled or delisted). Removing it.")
    prices = prices.drop(columns=empty)

    return prices
