from typing import List, Dict, Optional
import yfinance as yf
import pandas as pd


def get_realtime_data(ticker: str) -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period="1d", interval="1m") 
    return df.reset_index().dropna()

def get_data_between_dates(ticker: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end)
    return df.reset_index().dropna()

def get_data_from_start(ticker: str, start: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start)
    return df.reset_index().dropna()

def add_metrics(
  df: pd.DataFrame,
  sma_windows: List[int]  = [7,30],
  ema_windows: List[int]  = [7,30],
  vol_windows: List[int]  = [7]
) -> pd.DataFrame:
    for w in sma_windows:
        df[f"SMA_{w}"] = df["Close"].rolling(w).mean()
    for w in ema_windows:
        df[f"EMA_{w}"] = df["Close"].ewm(span=w, adjust=False).mean()
    for w in vol_windows:
        ret = df["Close"].pct_change()
        df[f"Vol_{w}"] = ret.rolling(w).std() * (252**0.5)
    return df

def process_stock_data(
  ticker: str,
  start: str,
  end: Optional[str] = None,
  mode: str = "history",
  sma_windows: List[int] = [7,30],
  ema_windows: List[int] = [7,30],
  vol_windows: List[int] = [7]
) -> pd.DataFrame:
    # …fetch df…
    return add_metrics(df, sma_windows, ema_windows, vol_windows)

