"""
@File         : trend.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-18 22:09:42
@Email        : cuixuanstephen@gmail.com
@Description  : 趋势信号
"""

import sys
from os import path

sys.path.append(path.normpath(path.join(path.dirname(__file__), "..")))
from utils.data_manipulate import add_column
import pandas as pd


def marubozu(
    data,
    open_column: int,
    high_column: int,
    low_column: int,
    close_column: int,
    buy_column,
    sell_column: int,
):
    # 算法很简单：
    # 1. 如果收盘价大于开盘价，并且收盘价等于最高价，开盘价等于最低价，那么就是看涨，下一交易日买入
    # 2. 如果收盘价低于开盘价，并且收盘价等于最低价，开盘价等于最高价，那么就是看跌，下一交易日卖出
    data = add_column(data, 5)
    for i in range(len(data)):
        try:
            if (
                data[i, close_column] > data[i, open_column]
                and data[i, high_column] == data[i, close_column]
                and data[i, low_column] == data[i, open_column]
                and data[i, buy_column] == 0
            ):
                data[i + 1, buy_column] = 1
            elif (
                data[i, close_column] < data[i, open_column]
                and data[i, high_column] == data[i, open_column]
                and data[i, close_column] == data[i, low_column]
                and data[i, sell_column] == 0
            ):
                data[i + 1, sell_column] = -1
        except IndexError:
            pass
    return data


def marubozu_pd(row: pd.DataFrame):
    if (
        row["Close"] > row["Open"]
        and row["High"] == row["Close"]
        and row["Low"] == row["Open"]
    ):
        return 1
    elif (
        row["Close"] < row["Open"]
        and row["High"] == row["Open"]
        and row["Close"] == row["Low"]
    ):
        return -1
    return 0


df = pd.read_csv("./data/510880 ETF Stock Price History.csv", parse_dates=["Date"])
df = df.rename({"Price": "Close"}, axis=1)
df = df.sort_values(by="Date", ascending=True, ignore_index=True)
# Signal 中的 1 表示当天出现了 marubozu，应该能搞操作的空间是在下一个交易日
df["Signal"] = df.apply(marubozu_pd, axis=1)
# df["Signal"] = df["Signal"].shift(1)

# import matplotlib.pyplot as plt

# mask_long = df["Signal"] == 1
# mask_short = df["Signal"] == -1
# fig, ax = plt.subplots(figsize=(15, 5))
# ax.plot(df["Close"], linewidth=0.5)
# ax.plot(df[mask_long]["Close"], marker="^", linestyle="None", color="red")
# ax.plot(df[mask_short]["Close"], marker="v", linestyle="None", color="purple")
