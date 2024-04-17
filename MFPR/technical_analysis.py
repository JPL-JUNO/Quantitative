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
from utils.data_manipulate import add_column, delete_row


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


if __name__ == "__main__":
    df = pd.read_csv("./data/510880 ETF Stock Price History.csv", parse_dates=["Date"])
    df = df.rename({"Price": "Close"}, axis=1)
    df = df.sort_values(by="Date", ignore_index=True)
