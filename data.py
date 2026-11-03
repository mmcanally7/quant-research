import pandas as pd
import yfinance as yf

def load_prices(tickers, start, end):
    """Adjusted daily closes, one column per ticker."""

    # Collect one DataFrame per ticker
    frames = []

    # Handle single ticker not a list
    if isinstance(tickers, str):
        tickers = [tickers]

    # Add prices here
    for ticker in tickers:
        ticker_prices = yf.download(ticker, start=start, end=end, auto_adjust=True)["Close"]
        frames.append(ticker_prices)

    # Convert to DataFrame
    prices = pd.concat(frames, axis=1)
    prices.columns = tickers

    # Drop tickers that returned no data
    empty = [t for t in tickers if prices[t].isna().all()]
    for ticker in empty:
        print(f"{ticker} is not in yfinance. Check spelling. Removing it.")
    prices = prices.drop(columns=empty)
    return prices
