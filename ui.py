import tkinter as tk

root =tk.Tk()

root.title("Stock Price Visualizer & Analyzer")
window_width= 1000
window_height= 650
# get screen info https://www.pythontutorial.net/tkinter/tkinter-window/
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


test= tk.Label(root, text="Welcome to Stock Market Analyzer and Visualizer")
test.pack()



root.mainloop()
