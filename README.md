# CIS298-Final-Project
CIS298 Intro to Python - 2025 (Final Project)

# Interactive Stock Price Visualizer & Analyzer

A Python-based GUI application that fetches historical stock market data and visualizes it using interactive, real-time graphs. Built with Plotly for dynamic charts and Tkinter for a modern interface, allows users to explore stock performance, compare companies, and apply basic financial analytics.

---

## Features

- Fetch historical stock data using `yfinance`
- Interactive Plotly graphs with zoom, hover, and pan
- Analytics overlays:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Volatility & Daily Returns (coming soon!)
- Clean GUI built with `Tkinter`
- Compare multiple stock tickers
- Export graphs to PNG & data to CSV

---

## Demo Video

![demo-video](assets/demo.video)

---

## Tech Stack

| Purpose         | Library           |
|----------------|-------------------|
| Stock Data      | [`yfinance`](https://pypi.org/project/yfinance/) |
| Data Handling   | [`pandas`](https://pandas.pydata.org/), [`datetime`](https://docs.python.org/3/library/datetime.html) |
| Visualization   | [`plotly`](https://github.com/plotly/plotly.py) |
| GUI             | [`tkinter`](https://docs.python.org/3/library/tk.html) |
| Export Options  | [`plotly.io`](https://plotly.com/python-api-reference/generated/plotly.io.html), [`os`](https://docs.python.org/3/library/os.html), [`csv`](https://docs.python.org/3/library/csv.html) |

---

## Installation

Clone the repo:
- git clone https://github.com/Mahoskian/CIS298-Final-Project.git
- cd CIS298-Final-Project
Create & activate a virtual environment:
- python -3.13 -m venv myenv
Enter Venv - On Windows:
- myenv\Scripts\activate
Install dependencies:
- pip install -r requirements.txt
Run the application:
- python main.py

