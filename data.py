import pandas as pd
import yfinance as yf


def load_prices(tickers, start, end):
    """
    Download daily adjusted closing prices from Yahoo Finance.

    tickers: a ticker string ("SPY") or a list of tickers (["SPY", "QQQ"]).
    start, end: dates as "YYYY-MM-DD" strings.
    Returns: DataFrame indexed by date, one column per ticker.
             Tickers with no data are dropped with a warning.

    Note: Yahoo has no history for delisted companies, so results
    for a list of today's stocks carry survivorship bias.
    """
    # Accept a single ticker as well as a list
    if isinstance(tickers, str):
        tickers = [tickers]

    # Collect one DataFrame per ticker
    frames = []
    for ticker in tickers:
        ticker_prices = yf.download(ticker, start=start, end=end, auto_adjust=True)["Close"]
        frames.append(ticker_prices)

    # Combine, aligning all tickers by date
    prices = pd.concat(frames, axis=1)
    prices.columns = tickers

    # Drop tickers that returned no data
    empty = [t for t in tickers if prices[t].isna().all()]
    for ticker in empty:
        print(f"{ticker}: no data from yfinance (misspelled or delisted). Removing it.")
    prices = prices.drop(columns=empty)

    return prices
