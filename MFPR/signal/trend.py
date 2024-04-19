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
import numpy as np


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


def three_candles(data, body, open_column, close_column, buy_column, sell_column):
    data = add_column(data, 5)

    for i in range(len(data)):
        try:
            # Bullish pattern
            bullish_1 = (data[i, close_column] - data[i, open_column]) > body
            bullish_2 = (data[i - 1, close_column] - data[i - 1, open_column]) > body
            bullish_3 = (data[i - 2, close_column] - data[i - 2, open_column]) > body
            bullish_4 = data[i, close_column] > data[i - 1, close_column]
            bullish_5 = data[i - 1, close_column] > data[i - 2, close_column]
            bullish_6 = data[i - 2, close_column] > data[i - 3, close_column]
            bullish_7 = data[i, buy_column] == 0
            if all(
                bullish_1,
                bullish_2,
                bullish_3,
                bullish_4,
                bullish_5,
                bullish_6,
                bullish_7,
            ):
                data[i + 1, buy_column] = 1
            bearish_1 = (data[i, close_column] < data[i - 1, close_column]) < body
            bearish_2 = (data[i - 1, close_column] < data[i - 2, close_column]) < body
            bearish_3 = (data[i - 2, close_column] < data[i - 3, close_column]) < body
            bearish_4 = (data[i, open_column] - data[i, close_column]) > body
            bearish_5 = (data[i - 1, open_column] - data[i - 1, close_column]) > body
            bearish_6 = (data[i - 2, open_column] - data[i - 2, close_column]) > body
            bearish_7 = data[i, sell_column] == 0
            # 如果我是买的不行嘛？当天表示为 1？可以，但是应该不会出现这种情况
            if all(
                bearish_1,
                bearish_2,
                bearish_3,
                bearish_4,
                bearish_5,
                bearish_6,
                bearish_7,
            ):
                data[i, sell_column] = -1
        except IndexError:
            pass


def three_candles_pd(data: pd.DataFrame, body=0.01) -> np.ndarray:
    rolled = data.rolling(window=4)
    signal = np.zeros(len(data))
    for idx, df in enumerate(rolled):
        if idx < 3:
            continue
        body_mask = all(((df["Close"] - df["Open"]).abs() > body).iloc[-3:])
        mask_up = all(df["Close"].diff().dropna() > 0)
        if body_mask and mask_up:
            signal[idx] = 1  # call 信号
            continue
        mask_down = all(df["Close"].diff().dropna() < 0)
        if body_mask and mask_down:
            signal[idx] = -1  # short 信号
    return signal


df = pd.read_csv("./data/510880 ETF Stock Price History.csv", parse_dates=["Date"])
df = df.rename({"Price": "Close"}, axis=1)
df = df.sort_values(by="Date", ascending=True, ignore_index=True)
# Signal 中的 1 表示当天出现了 marubozu，应该能搞操作的空间是在下一个交易日
# df["Signal"] = df.apply(marubozu_pd, axis=1)
# df["Signal"] = df["Signal"].shift(1)

import matplotlib.pyplot as plt

# bullish__long = df["Signal"] == 1
# bullish__short = df["Signal"] == -1
# fig, ax = plt.subplots(figsize=(15, 5))
# ax.plot(df["Close"], linewidth=0.5)
# ax.plot(df[bullish__long]["Close"], marker="^", linestyle="None", color="red")
# ax.plot(df[bullish__short]["Close"], marker="v", linestyle="None", color="purple")

signal = three_candles_pd(df)
df["signal"] = signal

fig, ax = plt.subplots(figsize=(18, 6))
ax.plot(df["Close"], linewidth=1, label="Close")
long = df["signal"] == 1
short = df["signal"] == -1
ax.plot(
    df[long]["Close"],
    marker="^",
    linestyle="None",
    color="red",
    markersize=2,
    label="Long",
)
ax.plot(
    df[short]["Close"],
    marker="v",
    linestyle="None",
    color="purple",
    markersize=2,
    label="Short",
)
plt.legend()
plt.title("510880 Three Candles")
plt.tight_layout()
plt.savefig("./figures/510880_three_candles.png", dpi=500)
