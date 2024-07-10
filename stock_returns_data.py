import yfinance as yf
import pandas as pd

def calculate_returns(df):
    """
    Calculate stock returns for different periods.

    Parameters:
    df (pd.DataFrame): DataFrame with stock prices, indexed by date.

    Returns:
    dict: A dictionary containing the stock returns for various periods.
    """
    stock_returns = {}
    today = df.index[-1]
    
    periods = {
        '1d': 2, # 1 day is not enough to calculate returns
        '7d': 7,
        '1m': 30,
        '3m': 90,
        '1y': 365,
    }

    for period, days in periods.items():
        if len(df) >= days:
            stock_returns[period] = f"{(df.iloc[-1] / df.iloc[-days] - 1)*100:.2f}%"
        else:
            stock_returns[period] = None

    # YTD
    start_of_year = pd.Timestamp(today.year, 1, 1)
    if start_of_year in df.index:
        stock_returns['ytd'] = f"{(df.iloc[-1] / df.loc[start_of_year] - 1)*100:.2f}%"
    else:
        stock_returns['ytd'] = None

    return stock_returns

def get_stock_returns_data(ticker):
    """
    Calculate returns for various periods for a given ticker.

    Parameters:
    ticker (str): Stock ticker symbol. For Brazilian stocks, '.SA' will be appended if not present.

    Returns:
    dict: A dictionary containing the stock returns for various periods including:
        1d, 1w, 1m, 3m, 1y, and ytd (Year to Date).
    """
    if not ticker.endswith('.SA'):
        ticker = ticker + '.SA'
    
    stock_data = yf.download(ticker, period='1y')['Close']
    
    all_days = pd.date_range(start=stock_data.index.min(), end=stock_data.index.max(), freq='D')
    
    stock_data = stock_data.reindex(all_days).ffill()

    stock_returns = calculate_returns(stock_data)

    return stock_returns