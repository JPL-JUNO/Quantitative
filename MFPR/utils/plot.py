"""
@File         : plot.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-16 21:18:06
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import matplotlib.pyplot as plt


def ohlc_plot_candles(data, window):
    sample = data[-window:,]
    for i, ohlc in enumerate(sample):
        plt.vlines(x=i, ymin=ohlc[2], ymax=ohlc[1], color="black", linewidth=1)
        if ohlc[3] > ohlc[0]: #收盘大于开盘，上涨
            plt.vlines(x=i, ymin=ohlc[0], ymax=ohlc[3], color="red", linewidth=3)
        if ohlc[3] < ohlc[0]:
            plt.vlines(x=i, ymin=ohlc[3], ymax=ohlc[0], color="green", linewidth=3)
        if ohlc[3] == ohlc[0]:
            plt.vlines(
                x=i, ymin=ohlc[3], ymax=ohlc[0] + 3e-5, color="black", linewidth=1.75
            )
    plt.grid()


if __name__ == "__main__":
    import pandas as pd
    from os import path
    import sys

    sys.path.append(path.join(path.dirname(__file__), "../"))
    from data.load_local_data import load_data

    data = load_data("EURUSD_wrangled")
    ohlc_plot_candles(data, 100)
