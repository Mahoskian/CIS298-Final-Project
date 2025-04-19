# main.py
import data_handler
import visualizer
import ui


def on_fetch():
    # Read ticker symbol and normalize
    ticker = ui.info.get().strip().upper()
    if not ticker:
        ui.root.bell()  # audible alert for missing input
        return

    # Read date range
    start = ui.dateStart.get_date().strftime("%Y-%m-%d")
    end = ui.dateEnd.get_date().strftime("%Y-%m-%d")

    # Fetch and process the data
    df = data_handler.process_stock_data(ticker, start, end)
    df_dict = {ticker: df}
    print(df_dict)

    # Determine which overlays to show based on checkboxes
    sma = ui.check1.instate(['selected'])
    ema = ui.check2.instate(['selected'])
    vol = ui.check3.instate(['selected'])

    # Create figure
    fig = visualizer.create_stock_figure(
        df_dict,
        sma_periods=[7] if sma else [],
        ema_periods=[30] if ema else [],
        show_volatility=vol,
        title=f"{ticker} Price & Metrics",
    )

    # Display the figure
    if fig is not None:
        fig.show()

if __name__ == "__main__":
    # Bind Fetch button and start UI
    ui.b.config(command=on_fetch)
    ui.root.mainloop()
