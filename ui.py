# ui.py
import tkinter as tk
import tkcalendar
from tkinter import ttk

root = tk.Tk()
root.tk.call('source', 'forest-dark.tcl')
ttk.Style().theme_use('forest-dark')

root.title("Stock Price Visualizer & Analyzer")
window_width, window_height = 600, 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.minsize=(600,600)
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


style=ttk.Style()

root.grid_columnconfigure((0,1,2), weight=1)
root.grid_rowconfigure((0,1,2),weight=1)

# widgets
label1=ttk.Label(root,
                 text="Welcome to Stock Market\nAnalyzer and Visualizer",
                 foreground="green",
                 font=("Arial Black", 15),
                 justify="center")
label1.grid(row=0,columnspan=3)

right_frame = ttk.Frame(root, padding=10)
right_frame.grid(row=1, column=1, rowspan=5, sticky="nw")


label2=ttk.Label(right_frame,
                 text="Select a Date Range\nand Ticker",
                 justify="center",
                 foreground="white",
                 font=("Arial Black",12))
dateStart = tkcalendar.DateEntry(right_frame)
dateEnd = tkcalendar.DateEntry(right_frame)

ticker_frame = ttk.Frame(right_frame)


max_tickers = 5
ticker_count = 0
ticker_rows = []                  # keep (row_frame, plus_button) pairs

def add_ticker_row():
    global ticker_count
    if ticker_count >= max_tickers:
        return
    # remove the old '+' from the previous row
    if ticker_rows:
        _, prev_btn = ticker_rows[-1]
        prev_btn.destroy()

    row = ttk.Frame(ticker_frame)
    entry = ttk.Entry(row)
    btn_plus = ttk.Button(row, text="+", width=2, command=add_ticker_row)

    entry.pack(side="left", fill="x", expand=True)
    btn_plus.pack(side="left", padx=(5,0))
    row.pack(fill="x", pady=2)

    ticker_rows.append((row, btn_plus))
    ticker_count += 1

# start with one row
add_ticker_row()


b = tk.Button(right_frame, text="Fetch", width=10,background="dark green")
for w in (label2, dateStart, dateEnd,ticker_frame, b):
    w.pack(fill="x", pady=5)

chk_frame = ttk.Frame(root, padding=5)
chk_frame.grid(row=1, column=0, sticky="ne", padx=5, pady=5)
check1 = ttk.Checkbutton(chk_frame, text="SMA")
check2 = ttk.Checkbutton(chk_frame, text="EMA")
check3 = ttk.Checkbutton(chk_frame, text="Volatility")

for chk in (check1, check2, check3):
    chk.pack(anchor="ne", pady=2)


# Dropdown for export


filetype=["CSV","PDF","PNG","JSON"]

exportFormat=ttk.Combobox(root,values=filetype)
exportFormat.set("Select Export Format")

exportFormat.grid(column=1, columnspan=2,row=1,sticky="ne",pady=73,padx=10)




