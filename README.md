# CIS298 - Python : Group 9 - Final Project : Winter 2025

# Interactive Stock Price Visualizer & Analyzer

A Python-based GUI application that fetches historical stock market data and visualizes it using interactive, real-time graphs. Built with Plotly for dynamic charts and Tkinter for a modern interface, allows users to explore stock performance, compare companies, and apply basic financial analytics.

---

## Authors & Contributions

- Soham Naik: Visualization
- Dilraj Dhillon: GUI
- Michael Asman: Data Handling

---

## Features

- Fetch historical stock data using `yfinance`
- Visual MatplotLib graphs
- Analytics overlays:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Volatility & Daily Returns (coming soon!)
- GUI built with `Tkinter`
- Compare multiple stock tickers
- Export graphs to PNG & data to CSV

---

## Demo Video

[▶️ Watch the Demo!](https://youtu.be/aHADO-xjKzM)

---

## Tech Stack

| Purpose         | Library           |
|----------------|-------------------|
| Stock Data      | [`yfinance`](https://pypi.org/project/yfinance/) |
| Data Handling   | [`pandas`](https://pandas.pydata.org/), [`datetime`](https://docs.python.org/3/library/datetime.html) |
| Visualization   | [`matplotlib`](https://matplotlib.org/) |
| GUI             | [`tkinter`](https://docs.python.org/3/library/tk.html) |
| Export Options  | [`os`](https://docs.python.org/3/library/os.html), [`csv`](https://docs.python.org/3/library/csv.html) |

---

## Installation

#### Clone the repo:
- git clone https://github.com/Mahoskian/CIS298-Final-Project.git
- cd CIS298-Final-Project
#### Create & activate a virtual environment:
- python -3.12 -m venv myenv
#### Enter Venv - On Windows:
- myenv\Scripts\activate
#### Install dependencies:
- pip install -r requirements.txt
#### Run the application:
- python app.py

