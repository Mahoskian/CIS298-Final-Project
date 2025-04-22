# 04/21/2025
# Soham Naik, Michael WR, Dilraj
# Check /references for the original code -> Ported into this file for ease of assembly.
# This script is a GUI application for fetching and visualizing stock data using yfinance.

import os
import json
from datetime import datetime, timedelta, date
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants for date limits and available metrics
MIN_DATE = date(2000, 1, 1)
TODAY = datetime.today().date()
MIN_SPAN_DAYS = 7
METRICS = ['Close', 'SMA', 'EMA', 'Volatility', 'Volume']


class DataHandler:
    # Manages fetching and processing stock data
    def __init__(self):
        self.data = {}

    def fetch(self, tickers):
        # Download history and compute indicators for each ticker
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        color_map = {t: colors[i % len(colors)] for i, t in enumerate(tickers)}
        self.data.clear()
        infos = []
        for t in tickers:
            obj = yf.Ticker(t)
            df = obj.history(period='max')
            if df is None or df.empty:
                infos.append(f"No data for {t}\n")
                continue
            # Calculate rolling and exponential moving averages
            df['SMA'] = df['Close'].rolling(20).mean()
            df['EMA'] = df['Close'].ewm(span=20, adjust=False).mean()
            # Calculate volatility as rolling std of returns
            df['Volatility'] = df['Close'].pct_change().rolling(20).std()
            self.data[t] = df
            info = obj.info or {}
            infos.append(self._format_info(t, info))
        return infos, color_map

    @staticmethod
    def _format_info(ticker, info):
        # Build a summary string of company info
        return (
            f"=== {ticker} ===\n"
            f"Name: {info.get('longName','N/A')}\n"
            f"Sector/Industry: {info.get('sector','N/A')} / {info.get('industry','N/A')}\n"
            f"Market Cap: {info.get('marketCap','N/A')} | PE: {info.get('trailingPE','N/A')}\n"
            f"EPS: {info.get('trailingEps','N/A')} | Div Yield: {info.get('dividendYield','N/A')}\n"
            f"Beta: {info.get('beta','N/A')}\n"
            f"Website: {info.get('website','N/A')}\n"
            f"Address: {info.get('address1','N/A')}, {info.get('city','N/A')}\n\n"
        )


class PlotManager:
    # Handles creation and updating of plot tabs
    def __init__(self, notebook):
        self.notebook = notebook
        self.tabs = {}
        self._create_tabs()

    def _create_tabs(self):
        # Set up an INFO tab for text summaries
        info_frame = ttk.Frame(self.notebook)
        info_text = tk.Text(info_frame, wrap='word', state='disabled')
        info_text.pack(fill='both', expand=True)
        self.tabs['INFO'] = {'frame': info_frame, 'widget': info_text}
        self.notebook.add(info_frame, text='INFO')
        # Create a tab for each metric with its own matplotlib canvas
        for metric in METRICS:
            frame = ttk.Frame(self.notebook)
            fig = plt.Figure(); fig.subplots_adjust(left=0.3)
            ax = fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack(fill='both', expand=True)
            self.tabs[metric] = {'frame': frame, 'ax': ax, 'fig': fig, 'canvas': canvas}
            self.notebook.add(frame, text=metric)

    def update(self, infos, data_values, color_map, start, end):
        # Refresh INFO tab with textual data
        widget = self.tabs['INFO']['widget']
        widget.config(state='normal')
        widget.delete('1.0', tk.END)
        widget.insert(tk.END, ''.join(infos))
        widget.config(state='disabled')
        # Redraw each metric's chart with the new data slice
        for metric, tab in self.tabs.items():
            if metric == 'INFO':
                continue
            ax = tab['ax']
            ax.clear()
            for t, df in data_values.items():
                sl = df.loc[start:end]
                if sl.empty:
                    sl = df
                ax.plot(sl.index, sl[metric], label=t, color=color_map[t])
            ax.set_title(metric)
            ax.legend(loc='center right', bbox_to_anchor=(-0.2, 0.5))
            tab['canvas'].draw()


class GUIManager:
    # Builds and manages all GUI widgets
    def __init__(self, root, controller):
        self.root = root
        self.ctrl = controller
        self._config_root()
        self._create_widgets()
        self._layout_widgets()
        self._bind_events()

    def _config_root(self):
        # Configure main window properties and apply dark theme if available
        self.root.title("Stock Data Viewer")
        try:
            self.root.state('zoomed')
        except:
            self.root.attributes('-zoomed', True)
        for i in range(4):
            self.root.columnconfigure(i, weight=1)
        self.root.rowconfigure(4, weight=1)
        try:
            self.root.tk.call('source', 'assets/forest-dark.tcl')
            ttk.Style(self.root).theme_use('forest-dark')
        except:
            pass

    def _create_widgets(self):
        # Instantiate all the widgets needed in the interface
        self.title_lbl = ttk.Label(self.root, text="Stock Data Viewer", font=(None, 16))
        self.ticker_frame = ttk.LabelFrame(self.root, text="Tickers")
        self.ticker_vars = []
        self._add_ticker()
        self.date_frame = ttk.Frame(self.root)
        self.start_cal = DateEntry(self.date_frame, width=12,
                                   mindate=MIN_DATE,
                                   maxdate=TODAY - timedelta(days=MIN_SPAN_DAYS))
        self.end_cal = DateEntry(self.date_frame, width=12,
                                 mindate=MIN_DATE,
                                 maxdate=TODAY)
        self.start_cal.set_date(TODAY - timedelta(days=MIN_SPAN_DAYS))
        self.end_cal.set_date(TODAY)
        self.ctrl_frame = ttk.Frame(self.root)
        self.fetch_btn = ttk.Button(self.ctrl_frame, text="Fetch", command=self.ctrl.on_fetch)
        self.export_combo = ttk.Combobox(self.ctrl_frame,
                                         values=["CSV", "Excel", "JSON", "PNG", "PDF"],
                                         state="readonly", width=6)
        self.export_combo.current(0)
        self.export_btn = ttk.Button(self.ctrl_frame, text="Export", command=self.ctrl.on_export)
        self.notebook = ttk.Notebook(self.root)

    def _layout_widgets(self):
        # Position all widgets using grid and pack geometry managers
        self.title_lbl.grid(row=0, column=0, columnspan=4, sticky='w', padx=10, pady=5)
        self.ticker_frame.grid(row=1, column=0, columnspan=4, sticky='we', padx=10, pady=5)
        ttk.Label(self.date_frame, text="Range -> Start Date:").pack(side='left')
        self.start_cal.pack(side='left', padx=5)
        ttk.Label(self.date_frame, text="End Date:").pack(side='left')
        self.end_cal.pack(side='left', padx=5)
        self.date_frame.grid(row=2, column=0, columnspan=4, sticky='w', padx=10)
        self.fetch_btn.pack(side='left')
        self.export_combo.pack(side='left', padx=5)
        self.export_btn.pack(side='left')
        self.ctrl_frame.grid(row=3, column=0, columnspan=4, sticky='w', padx=10, pady=5)
        self.notebook.grid(row=4, column=0, columnspan=4, sticky='nsew', padx=10, pady=5)

    def _add_ticker(self):
        # Add a new ticker entry field
        var = tk.StringVar()
        self.ticker_vars.append(var)
        self._refresh_tickers()

    def _refresh_tickers(self):
        # Rebuild ticker entry row to show + and - buttons correctly
        for w in self.ticker_frame.winfo_children():
            w.destroy()
        for i, var in enumerate(self.ticker_vars):
            ttk.Entry(self.ticker_frame, textvariable=var, width=8).grid(row=0, column=i*2, padx=2, pady=2)
            if i > 0:
                ttk.Button(self.ticker_frame, text='-', width=2,
                           command=lambda v=var: self.ctrl.on_remove_ticker(v)).grid(
                    row=0, column=i*2+1, padx=2)
            if i == len(self.ticker_vars) - 1:
                ttk.Button(self.ticker_frame, text='+', width=2,
                           command=self.ctrl.on_add_ticker).grid(row=0, column=i*2+1, padx=2)

    def _bind_events(self):
        # Hook date pickers to dropdown and change events
        for cal in (self.start_cal, self.end_cal):
            cal.bind('<Button-1>', lambda e, c=cal: c.drop_down())
            cal.bind('<<DateEntrySelected>>', lambda e: self.ctrl.on_date_change(e))

    def get_tickers(self):
        # Return list of cleaned ticker symbols
        return [v.get().strip().upper() for v in self.ticker_vars if v.get().strip()]

    def get_date_range(self):
        # Return formatted start and end dates
        return (self.start_cal.get_date().strftime('%Y-%m-%d'),
                self.end_cal.get_date().strftime('%Y-%m-%d'))

    def get_export_format(self):
        # Return currently selected export format
        return self.export_combo.get()


class StockApp:
    # Orchestrates data, GUI, and plotting components
    def __init__(self, root):
        self.data_handler = DataHandler()
        self.gui = GUIManager(root, self)
        self.plot_mgr = PlotManager(self.gui.notebook)
        self.infos = []
        self.color_map = {}

    def on_add_ticker(self):
        # Delegate to GUI to add a ticker field
        self.gui._add_ticker()

    def on_remove_ticker(self, var):
        # Remove a ticker field and refresh layout
        self.gui.ticker_vars.remove(var)
        self.gui._refresh_tickers()

    def on_date_change(self, event):
        # Enforce minimum span between dates and update plot if needed
        start_date = self.gui.start_cal.get_date()
        end_date = self.gui.end_cal.get_date()
        if event.widget == self.gui.end_cal:
            min_end = start_date + timedelta(days=MIN_SPAN_DAYS)
            if end_date < min_end:
                self.gui.end_cal.set_date(min_end)
        else:
            max_start = end_date - timedelta(days=MIN_SPAN_DAYS)
            if start_date > max_start:
                self.gui.start_cal.set_date(max_start)
        if self.data_handler.data:
            start, end = self.gui.get_date_range()
            self.plot_mgr.update(self.infos, self.data_handler.data, self.color_map, start, end)

    def on_fetch(self):
        # Fetch data for entered tickers and update plots
        tickers = self.gui.get_tickers()
        if not tickers:
            messagebox.showwarning("No Tickers", "Enter at least one ticker.")
            return
        self.infos, self.color_map = self.data_handler.fetch(tickers)
        start, end = self.gui.get_date_range()
        self.plot_mgr.update(self.infos, self.data_handler.data, self.color_map, start, end)

    def on_export(self):
        # Export current data or chart in selected format
        fmt = self.gui.get_export_format()
        start, end = self.gui.get_date_range()
        ticks = self.gui.get_tickers()
        filename = f"{datetime.now():%Y%m%d}-{start.replace('-', '')}-{end.replace('-', '')}[{'-'.join(ticks)}]"
        out_dir = os.path.join(os.path.dirname(__file__), 'export')
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"{filename}.{fmt.lower()}")
        if fmt == 'JSON':
            data_out = {
                t: df.reset_index().rename(columns={df.index.name: 'Date'})
                       .assign(Date=lambda x: x['Date'].dt.strftime('%Y-%m-%d'))
                       .to_dict(orient='records')
                for t, df in self.data_handler.data.items()
            }
            with open(path, 'w') as f:
                json.dump(data_out, f, indent=4)
        elif fmt == 'CSV':
            pd.concat(self.data_handler.data, names=['Ticker','Date']).to_csv(path)
        elif fmt == 'Excel':
            with pd.ExcelWriter(path) as writer:
                for t, df in self.data_handler.data.items():
                    df.to_excel(writer, sheet_name=t)
        else:
            current = self.gui.notebook.tab(self.gui.notebook.select(), 'text')
            if current == 'INFO':
                widget = self.plot_mgr.tabs['INFO']['widget']
                with open(path, 'w') as f:
                    f.write(widget.get('1.0', tk.END))
            else:
                self.plot_mgr.tabs[current]['fig'].savefig(path)
        messagebox.showinfo('Export', f'Data exported to {path}')


if __name__ == '__main__':
    # Entry point: create the main window and run the app
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
