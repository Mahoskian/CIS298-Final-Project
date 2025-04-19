# Soham Naik - 04/18/2025
# visualizer.py
# Module for creating interactive stock visualizations using Plotly
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from typing import Dict, List, Optional

def calculate_sma(df: pd.DataFrame, window: int) -> pd.Series:
    #Calculate Simple Moving Average (SMA) over a specified window.
    return df['Close'].rolling(window=window).mean()


def calculate_ema(df: pd.DataFrame, window: int) -> pd.Series:
    #Calculate Exponential Moving Average (EMA) over a specified window.
    return df['Close'].ewm(span=window, adjust=False).mean()


def calculate_volatility(df: pd.DataFrame, window: int) -> pd.Series:
    #Calculate annualized volatility based on rolling standard deviation of returns.
    returns = df['Close'].pct_change()
    return returns.rolling(window=window).std() * (252 ** 0.5)


def create_stock_figure(
    df_dict: Dict[str, pd.DataFrame],
    sma_periods: Optional[List[int]] = None,
    ema_periods: Optional[List[int]] = None,
    show_volatility: bool = False,
    vol_period: int = 20,
    title: str = "Stock Price Chart",
    template: str = "plotly_white"
) -> go.Figure:
    # Create an interactive Plotly figure for one or more stocks.
    fig = go.Figure()

    # Iterate through each ticker's data
    for ticker, df in df_dict.items():
        # Ensure datetime index
        df = df.sort_index()

        # Close price line
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Close'],
            mode='lines',
            name=f"{ticker} Close",
            hovertemplate='%{y:.2f}<br>%{x}<extra></extra>'
        ))

        # Volume as bar (secondary axis)
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['Volume'],
            name=f"{ticker} Volume",
            yaxis='y2',
            opacity=0.3,
            marker=dict(line=dict(width=0)),
            hovertemplate='%{y}<br>%{x}<extra></extra>'
        ))

        # Simple Moving Averages
        if sma_periods:
            for window in sma_periods:
                sma = calculate_sma(df, window)
                fig.add_trace(go.Scatter(
                    x=sma.index,
                    y=sma,
                    mode='lines',
                    name=f"{ticker} SMA {window}",
                    line=dict(dash='dot'),
                    hovertemplate='%{y:.2f}<br>%{x}<extra></extra>'
                ))

        # Exponential Moving Averages
        if ema_periods:
            for window in ema_periods:
                ema = calculate_ema(df, window)
                fig.add_trace(go.Scatter(
                    x=ema.index,
                    y=ema,
                    mode='lines',
                    name=f"{ticker} EMA {window}",
                    line=dict(dash='dash'),
                    hovertemplate='%{y:.2f}<br>%{x}<extra></extra>'
                ))

        # Volatility overlay
        if show_volatility:
            vol = calculate_volatility(df, vol_period)
            fig.add_trace(go.Scatter(
                x=vol.index,
                y=vol,
                mode='lines',
                name=f"{ticker} Volatility {vol_period}",
                yaxis='y3',
                hovertemplate='%{y:.4f}<br>%{x}<extra></extra>'
            ))

    # Configure layout with multiple y-axes
    fig.update_layout(
        title=title,
        xaxis=dict(title='Date', type='date', rangeslider=dict(visible=True)),
        yaxis=dict(title='Price', side='left', showgrid=False),
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False,
            position=1.0
        ),
        yaxis3=dict(
            title='Volatility',
            overlaying='y',
            side='right',
            showgrid=False,
            position=0.85
        ),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        template=template,
        margin=dict(l=50, r=80, t=50, b=50)
    )

    return fig


def export_figure_to_png(fig: go.Figure, filename: str, width: int = 1200, height: int = 800):
    # Export a Plotly figure to a PNG file using Kaleido.
    try:
        pio.write_image(fig, filename, width=width, height=height)
        print(f"Exported figure to {filename}")
    except Exception as e:
        print(f"Error exporting figure: {e}")


def display_data_summary(df_dict: Dict[str, pd.DataFrame]):
    # Print basic summary statistics for each ticker's DataFrame.
    for ticker, df in df_dict.items():
        print(f"--- {ticker} Data Summary ---")
        print(df.describe(), "\n")
