"""
@File         : technical_analysis.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-17 19:45:50
@Email        : cuixuanstephen@gmail.com
@Description  : 技术分析指标
"""

import pandas as pd
import numpy as np
import sys
from os import path

sys.path.append(path.normpath(path.join(path.dirname(__file__), "..")))
from utils.indicators import add_column, delete_row, delete_column


def ma(data: np.array, lookback: int, close: int, position: int):
    data = add_column(data, 1)
    for i in range(lookback - 1, len(data)):
        data[i, position] = data[i - lookback + 1 : i + 1, close].mean()
        # try:
        #     data[i, position] = data[i - lookback + 1 : i + 1, close].mean()
        # except IndexError:
        #     pass
    data = delete_row(data, lookback)
    return data


def ma_pd(data: pd.DataFrame, window: int, close_index: int, target_index: int):
    pass


def smoothed_ma(data: np.ndarray, alpha: float, lookback, close, position):
    lookback = 2 * lookback - 1
    alpha = alpha / (lookback + 1.0)
    beta = 1 - alpha
    data = ma(data, lookback, close, position)

    data[lookback + 1, position] = (
        data[lookback + 1, close] * alpha + data[lookback, position] * beta
    )
    for i in range(lookback + 2, len(data)):
        try:
            data[i, position] = data[i, close] * alpha + data[i - 1, position] * beta
        except IndexError:
            pass

    return data


def rsi(data, lookback, close, position):
    data = add_column(data, 5)
    for i in range(len(data)):
        data[i, position] = data[i, close] - data[i - 1, close]
    for i in range(len(data)):
        if data[i, position] > 0:
            data[i, position + 1] = data[i, position]
        elif data[i, position] < 0:
            data[i, position + 2] = abs(data[i, position])
    data = smoothed_ma(data, 2, lookback, position + 1, position + 3)
    data = smoothed_ma(data, 2, lookback, position + 2, position + 4)
    data[:, position + 5] = data[:, position + 3] / data[:, position + 4]

    data = delete_column(data, position, 6)
    data = delete_row(data, lookback)

    return data


if __name__ == "__main__":
    df = pd.read_csv("./data/510880 ETF Stock Price History.csv", parse_dates=["Date"])
    df = df.rename({"Price": "Close"}, axis=1)
    df = df.sort_values(by="Date", ignore_index=True)
