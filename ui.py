# ui.py
import tkinter as tk
import tkcalendar
from tkinter import ttk

root = tk.Tk()
root.tk.call('source', 'forest-dark.tcl')
ttk.Style().theme_use('forest-dark')

root.title("Stock Price Visualizer & Analyzer")
window_width, window_height = 500, 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# header
tk.Label(root, text="Welcome to Stock Market Analyzer and Visualizer").pack()

# controls container
cont = ttk.Frame(root)
cont.pack(pady=(15,150), padx=30)

info = tk.Entry(cont)
info.pack(side="top", padx=(20,0), pady=(145,20))

b = tk.Button(cont, text="Fetch", height=2, width=10)
b.pack(side="right")

check1 = ttk.Checkbutton(cont, text="SMA")
check2 = ttk.Checkbutton(cont, text="EMA")
check3 = ttk.Checkbutton(cont, text="Volatility")
for chk in (check1, check2, check3):
    chk.pack(padx=(0,10))

# date pickers
tk.Label(root, text="Select a Date Range").pack()
dateStart = tkcalendar.DateEntry(root)
dateStart.pack()
dateEnd = tkcalendar.DateEntry(root)
dateEnd.pack()
