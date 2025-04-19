import yfinance as yf
import pandas as pd
import datetime as dt
import tkinter as tk
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import plotly.subplots as sp
import os
import csv
from datetime import datetime


from data_handler import process_stock_data

if __name__ == "__main__":
    df = process_stock_data("MSFT", start="2024-01-01", end="2024-03-01")
    print(df.tail())