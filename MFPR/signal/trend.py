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


def tasuki(data, open_column, close_column: int, buy_column: int, sell_column: int):
    data = add_column(data, 5)
    for i in range(len(data)):
        try:
            # Bullish pattern
            if (
                data[i, close_column] < data[i, open_column]
                and data[i, close_column] < data[i - 1, open_column]
                and data[i, close_column] > data[i - 2, close_column]
                and data[i - 1, close_column] > data[i - 1, open_column]
                and data[i - 1, open_column] > data[i - 2, close_column]
                and data[i - 2, close_column] > data[i - 2, open_column]
            ):
                data[i + 1, buy_column] = 1
            # Bearish pattern
            elif (
                data[i, close_column] > data[i, open_column]
                and data[i, close_column] > data[i - 1, open_column]
                and data[i, close_column] < data[i - 2, close_column]
                and data[i - 1, close_column] < data[i - 1, open_column]
                and data[i - 1, open_column] < data[i - 2, close_column]
                and data[i - 2, close_column] < data[i - 2, open_column]
            ):
                data[i + 1, sell_column] = -1
        except IndexError:
            pass


def tasuki_pd(data: pd.DataFrame):
    rolled = data.rolling(window=3)
    signal = np.zeros(len(data))
    up_down = pd.Series([True, True, False])
    for idx, df in enumerate(rolled):
        if idx < 2:
            continue
        # 前两个应该是阳线，第三个是阴线
        up_down.index = df.index
        mask1_up = (df["Close"] > df["Open"]).equals(up_down)  # 基于索引的比较
        gap = df["Open"].iloc[1] > df["Close"].iloc[0]  # 跳开（多）
        mask2_up = df["Close"].iloc[0] < df["Close"].iloc[2] < df["Open"].iloc[1]
        if mask1_up and gap and mask2_up:
            signal[idx] = 1
            continue
        # 阴线、阴线、阳线
        mask1_down = (df["Close"] < df["Open"]).equals(up_down)
        gap_down = df["Open"].iloc[1] < df["Close"].iloc[0]  # 跳开（空）
        mask2_down = df["Open"].iloc[1] < df["Close"].iloc[2] < df["Close"].iloc[0]
        if mask1_down and gap_down and mask2_down:
            signal[idx] = -1

    return signal


def three_methods(
    data, open_column, high_column, low_column, close_column, buy_column, sell_column
):
    data = add_column(data, 5)
    for i in range(len(data)):
        try:
            # Bullish pattern
            if (
                data[i, close_column] > data[i, open_column]
                and data[i, close_column] > data[i - 4, high_column]
                and data[i, low_column] < data[i - 1, low_column]
                and data[i - 1, close_column] < data[i - 4, close_column]
                and data[i - 1, low_column] > data[i - 4, low_column]
                and data[i - 2, close_column] < data[i - 4, close_column]
                and data[i - 2, low_column] > data[i - 4, low_column]
                and data[i - 3, close_column] < data[i - 4, close_column]
                and data[i - 3, low_column] > data[i - 4, low_column]
                and data[i - 4, close_column] > data[i - 4, open_column]
            ):
                data[i + 1, buy_column] = 1
            # Bearish pattern
            elif (
                data[i, close_column] < data[i, open_column]
                and data[i, close_column] < data[i - 4, high_column]
                and data[i, high_column] > data[i - 1, high_column]
                and data[i - 1, close_column] > data[i - 4, close_column]
                and data[i - 1, high_column] < data[i - 4, high_column]
                and data[i - 2, close_column] > data[i - 4, close_column]
                and data[i - 2, high_column] < data[i - 4, high_column]
                and data[i - 3, close_column] > data[i - 4, close_column]
                and data[i - 3, high_column] < data[i - 4, high_column]
            ):
                data[i + 1, sell_column] = -1
        except IndexError:
            pass
    pass


def three_methods_pd(data: pd.DataFrame) -> np.ndarray:
    # 此方法不确定具体的实现方式
    # CONFIRM
    rolled = data.rolling(window=5)
    signal = np.zeros(len(data))
    up_down = pd.Series([True, False, False, False, True])
    for idx, df in enumerate(rolled):
        if idx < 4:
            continue
        up_down.index = df.index
        # 满足阳、阴阴阴、阳的线
        mask1 = (df["Close"] > df["Open"]).equals(up_down)
        above_low = all(df["Low"].iloc[1:4] > df["Low"].iloc[0])
        below_high = all(df["High"].iloc[1:4] < df["High"].iloc[0])
        mask2 = df["Close"].iloc[-1] > df["High"].iloc[0]
        mask3 = df["Low"].iloc[-1] < df["Low"].iloc[-2]
        if mask1 and below_high and above_low and mask2 and mask3:
            signal[idx] = 1
            continue
        mask1 = (df["Close"] < df["Open"]).equals(up_down)
        mask2 = df["Close"].iloc[-1] < df["Low"].iloc[0]
        mask3 = df["High"].iloc[-1] > df["High"].iloc[-2]
        if mask1 and above_low and below_high and mask2 and mask3:
            signal[idx] = -1
    return signal


if __name__ == "__main__":
    underlying = "CSI300"
    df = pd.read_csv(f"./data/A/{underlying}.csv", parse_dates=["Date"], thousands=",")
    df = df.rename({"Price": "Close"}, axis=1)
    df = df.sort_values(by="Date", ascending=True, ignore_index=True)
    # Signal 中的 1 表示当天出现了 marubozu，应该能搞操作的空间是在下一个交易日
    # df["Signal"] = df.apply(marubozu_pd, axis=1)
    # df["Signal"] = df["Signal"].shift(1)
    # signal = tasuki_pd(df)
    # df["signal"] = signal
    # import matplotlib.pyplot as plt

    # # bullish__long = df["Signal"] == 1
    # # bullish__short = df["Signal"] == -1
    # # fig, ax = plt.subplots(figsize=(15, 5))
    # # ax.plot(df["Close"], linewidth=0.5)
    # # ax.plot(df[bullish__long]["Close"], marker="^", linestyle="None", color="red")
    # # ax.plot(df[bullish__short]["Close"], marker="v", linestyle="None", color="purple")

    # # signal = three_candles_pd(df)
    # # df["signal"] = signal

    # fig, ax = plt.subplots(figsize=(18, 6))
    # ax.plot(df["Close"], linewidth=1, label="Close")
    # long = df["signal"] == 1
    # short = df["signal"] == -1
    # ax.plot(
    #     df[long]["Close"],
    #     marker="^",
    #     linestyle="None",
    #     color="red",
    #     markersize=4,
    #     label="Long",
    # )
    # ax.plot(
    #     df[short]["Close"],
    #     marker="v",
    #     linestyle="None",
    #     color="purple",
    #     markersize=4,
    #     label="Short",
    # )
    # plt.legend()
    # plt.title(f"{underlying} Three Candles")
    # plt.tight_layout()
    # plt.savefig(f"./figures/{underlying}_tasuki.png", dpi=500)
