

import yfinance as yf
import pandas as pd

# 1. Fetch real-time (latest day) data
def get_realtime_data(ticker: str) -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period="1d", interval="1m")  # 1-minute interval for the current day
    return df.reset_index().dropna()

# 2. Fetch historical data between two dates
def get_data_between_dates(ticker: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end)
    return df.reset_index().dropna()

# 3. Fetch data from a start date to today
def get_data_from_start(ticker: str, start: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start)
    return df.reset_index().dropna()

# 4. Add computed metrics: moving averages, returns, volatility
def add_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df['7_day_MA'] = df['Close'].rolling(window=7).mean()
    df['30_day_MA'] = df['Close'].rolling(window=30).mean()
    df['Daily_Return'] = df['Close'].pct_change()
    df['Volatility_7d'] = df['Daily_Return'].rolling(window=7).std()
    return df

# 5. Main function for full processing
def process_stock_data(ticker: str, start: str, end: str = None, mode: str = 'history') -> pd.DataFrame:
    """
    mode: 'realtime', 'history', or 'from_start'
    """
    if mode == 'realtime':
        df = get_realtime_data(ticker)
    elif mode == 'from_start':
        df = get_data_from_start(ticker, start)
    else:
        df = get_data_between_dates(ticker, start, end)

    df = add_metrics(df)
    return df
