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

# Constants
MIN_DATE = date(2000, 1, 1)
TODAY = datetime.today().date()
MIN_SPAN_DAYS = 7
METRICS = [
    'Close', 'SMA', 'EMA', 'Volatility', 'Volume'
]

class StockApp:
    def __init__(self, root):
        self.root = root
        self._configure_root()
        self._create_widgets()
        self._layout_widgets()
        self._bind_events()

        # Internal state
        self.data_full = {}
        self.color_map = {}

    def _configure_root(self):
        self.root.title("Stock Data Viewer")
        # Maximize window
        try:
            self.root.state('zoomed')
        except:
            self.root.attributes('-zoomed', True)
        for i in range(4): self.root.columnconfigure(i, weight=1)
        self.root.rowconfigure(4, weight=1)
        # Load theme
        try:
            self.root.tk.call('source', 'forest-dark.tcl')
            ttk.Style(self.root).theme_use('forest-dark')
        except:
            pass

    def _create_widgets(self):
        # Title
        self.title_lbl = ttk.Label(self.root, text="Stock Data Viewer", font=(None,16))
        # Tickers
        self.ticker_frame = ttk.LabelFrame(self.root, text="Tickers")
        self.ticker_vars = []
        self.add_ticker()
        # Date range
        self.date_frame = ttk.Frame(self.root)
        self.start_cal = DateEntry(
            self.date_frame, width=12,
            mindate=MIN_DATE,
            maxdate=TODAY - timedelta(days=MIN_SPAN_DAYS)
        )
        self.end_cal = DateEntry(
            self.date_frame, width=12,
            mindate=MIN_DATE,
            maxdate=TODAY
        )
        self.start_cal.set_date(TODAY - timedelta(days=MIN_SPAN_DAYS))
        self.end_cal.set_date(TODAY)
        # Controls
        self.ctrl_frame = ttk.Frame(self.root)
        self.fetch_btn = ttk.Button(self.ctrl_frame, text="Fetch", command=self.fetch_data)
        self.export_combo = ttk.Combobox(
            self.ctrl_frame, values=["CSV","Excel","JSON","PNG","PDF"],
            state="readonly", width=6
        )
        self.export_combo.current(0)
        self.export_btn = ttk.Button(self.ctrl_frame, text="Export", command=self.export_data)
        # Notebook
        self.notebook = ttk.Notebook(self.root)
        self.tabs = {}
        # INFO tab
        info_frame = ttk.Frame(self.notebook)
        info_text = tk.Text(info_frame, wrap='word', state='disabled')
        info_text.pack(fill='both', expand=True)
        self.tabs['INFO'] = {'frame': info_frame, 'widget': info_text}
        self.notebook.add(info_frame, text='INFO')
        # Metric tabs
        for metric in METRICS:
            frame = ttk.Frame(self.notebook)
            fig = plt.Figure(); fig.subplots_adjust(left=0.3)
            ax = fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack(fill='both', expand=True)
            self.tabs[metric] = {'frame': frame, 'ax': ax, 'fig': fig, 'canvas': canvas}
            self.notebook.add(frame, text=metric)

    def _layout_widgets(self):
        self.title_lbl.grid(row=0, column=0, columnspan=4, sticky='w', padx=10, pady=5)
        self.ticker_frame.grid(row=1, column=0, columnspan=4, sticky='we', padx=10, pady=5)
        # Date labels + entries inline
        ttk.Label(self.date_frame, text="Range -> Start Date:").pack(side='left')
        self.start_cal.pack(side='left', padx=5)
        ttk.Label(self.date_frame, text="End Date:").pack(side='left')
        self.end_cal.pack(side='left', padx=5)
        self.date_frame.grid(row=2, column=0, columnspan=4, sticky='w', padx=10)
        # Controls
        self.fetch_btn.pack(side='left')
        self.export_combo.pack(side='left', padx=5)
        self.export_btn.pack(side='left')
        self.ctrl_frame.grid(row=3, column=0, columnspan=4, sticky='w', padx=10, pady=5)
        # Notebook
        self.notebook.grid(row=4, column=0, columnspan=4, sticky='nsew', padx=10, pady=5)

    def _bind_events(self):
        # Calendar popups
        for cal in (self.start_cal, self.end_cal):
            cal.bind('<Button-1>', lambda e, c=cal: self._open_calendar(c))
            cal.bind('<<DateEntrySelected>>', self.on_date_change)

    def _open_calendar(self, cal):
        cal.drop_down()
        # disable auto-close on focus-out
        try:
            cal._calendar.unbind('<FocusOut>')
            cal._top_cal.unbind('<FocusOut>')
        except:
            pass

    def on_date_change(self, event):
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        if event.widget == self.end_cal:
            min_end = start + timedelta(days=MIN_SPAN_DAYS)
            if end < min_end:
                self.end_cal.set_date(min_end)
        else:
            max_start = end - timedelta(days=MIN_SPAN_DAYS)
            if start > max_start:
                self.start_cal.set_date(max_start)
        if self.data_full:
            self.update_tabs()

    def refresh_tickers(self):
        for w in self.ticker_frame.winfo_children(): w.destroy()
        for i, var in enumerate(self.ticker_vars):
            ttk.Entry(self.ticker_frame, textvariable=var, width=8).grid(
                row=0, column=i*2, padx=2, pady=2)
            if i > 0:
                ttk.Button(
                    self.ticker_frame, text='-', width=2,
                    command=lambda v=var: self.remove_ticker(v)
                ).grid(row=0, column=i*2+1, padx=2)
            if i == len(self.ticker_vars) - 1:
                ttk.Button(
                    self.ticker_frame, text='+', width=2,
                    command=self.add_ticker
                ).grid(row=0, column=i*2+1, padx=2)

    def add_ticker(self):
        self.ticker_vars.append(tk.StringVar())
        self.refresh_tickers()

    def remove_ticker(self, var):
        self.ticker_vars.remove(var)
        self.refresh_tickers()

    def fetch_data(self):
        tickers = [v.get().strip().upper() for v in self.ticker_vars if v.get().strip()]
        if not tickers:
            messagebox.showwarning("No Tickers", "Please enter at least one ticker.")
            return
        # assign colors
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        self.color_map = {t: colors[i % len(colors)] for i, t in enumerate(tickers)}
        self.data_full.clear()
        info_list = []
        for t in tickers:
            obj = yf.Ticker(t)
            df = obj.history(period='max')
            if df is None or df.empty:
                info_list.append(f"No data for {t}\n")
                continue
            # compute metrics
            df['SMA'] = df['Close'].rolling(20).mean()
            df['EMA'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['Volatility'] = df['Close'].pct_change().rolling(20).std()
            self.data_full[t] = df
            info = obj.info or {}
            info_list.append(self._format_info(t, info))
        # update INFO tab
        widget = self.tabs['INFO']['widget']
        widget.config(state='normal')
        widget.delete('1.0', tk.END)
        widget.insert(tk.END, "".join(info_list))
        widget.config(state='disabled')
        # plot
        self.update_tabs()

    def _format_info(self, ticker, info):
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

    def update_tabs(self):
        s = self.start_cal.get_date().strftime('%Y-%m-%d')
        e = self.end_cal.get_date().strftime('%Y-%m-%d')
        for metric, tab in self.tabs.items():
            if metric == 'INFO': continue
            ax = tab['ax']
            ax.clear()
            for t, df in self.data_full.items():
                sl = df.loc[s:e]
                if sl.empty:
                    sl = df
                ax.plot(sl.index, sl[metric], label=t, color=self.color_map[t])
            ax.set_title(metric)
            ax.legend(loc='center right', bbox_to_anchor=(-0.2,0.5))
            tab['canvas'].draw()

    def export_data(self):
        fmt = self.export_combo.get()
        s = self.start_cal.get_date().strftime('%Y%m%d')
        e = self.end_cal.get_date().strftime('%Y%m%d')
        ticks = [v.get().strip().upper() for v in self.ticker_vars if v.get().strip()]
        filename = f"{datetime.now():%Y%m%d}-{s}-{e}[{'-'.join(ticks)}]"
        out_dir = os.path.join(os.path.dirname(__file__), 'export')
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"{filename}.{fmt.lower()}")
        if fmt == 'JSON':
            data_out = {
                t: df.reset_index().rename(columns={df.index.name: 'Date'})
                          .assign(Date=lambda x: x['Date'].dt.strftime('%Y-%m-%d'))
                          .to_dict(orient='records')
                for t, df in self.data_full.items()
            }
            with open(path, 'w') as f:
                json.dump(data_out, f, indent=4)
        elif fmt == 'CSV':
            pd.concat(self.data_full, names=['Ticker','Date']).to_csv(path)
        elif fmt == 'Excel':
            with pd.ExcelWriter(path) as writer:
                for t, df in self.data_full.items():
                    df.to_excel(writer, sheet_name=t)
        else:
            current = self.notebook.tab(self.notebook.select(), 'text')
            if current == 'INFO':
                widget = self.tabs['INFO']['widget']
                with open(path, 'w') as f:
                    f.write(widget.get('1.0', tk.END))
            else:
                self.tabs[current]['fig'].savefig(path)
        messagebox.showinfo('Export', f'Data exported to {path}')

if __name__ == '__main__':
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
