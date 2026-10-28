import pandas as pd

def drawdown_stats(prices):
    """
    Max drawdown, bottom date, and recovery date for a price series.

    prices: pandas Series (or one-column DataFrame) of prices, indexed by date.
    Returns: (max_dd, bottom_date, recovery_date); recovery_date is None
             if the price has not regained its prior peak.
    """
    # Make a series from DataFrame if necessary
    if isinstance(prices, pd.DataFrame):
        prices=prices.iloc[:,0]

    # Compute max drawdown
    running_peak = prices.cummax()
    drawdown = prices/running_peak - 1

    # Compute bottom date
    bottom_date = drawdown.idxmin()
    max_dd = drawdown.min()

    # Compute recovery date
    after_bottom = drawdown.loc[bottom_date:]
    recovery = after_bottom[after_bottom == 0]
    if recovery.empty:
        recovery_date = None
        print("The stock has yet to recover.")
    else:
        recovery_date = recovery.index[0]

    return max_dd, bottom_date, recovery_date
