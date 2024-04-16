"""
@Title        : 
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2023-12-29 21:02:25
@Description  : 
"""

from pandas import DataFrame
import datetime
import pytz
import pandas as pd
import MetaTrader5 as mt5
import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray

frame_H1 = mt5.TIMEFRAME_H1
frame_D1 = mt5.TIMEFRAME_D1

now = datetime.datetime.now()

asserts = [
    "EURUSD",
    "USDCHF",
    "GBPUSD",
    "USDCAD",
    "BTCUSD",
    "ETHUSD",
    "XAUUSD",
    "SP500m",
    "UK100",
]


def mass_import(asset: int = 0, time_frame: str = "D1") -> ndarray:
    if time_frame == "H1":
        data = get_quotes(frame_H1, 2013, 1, 1, asset=asserts[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals=5)

    if time_frame == "D1":
        data = get_quotes(frame_D1, 2000, 1, 1, asset=asserts[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals=5)

    return data


def get_quotes(
    time_frame, year: int = 2017, month: int = 1, day: int = 1, asset="EURUSD"
):

    if not mt5.initialize():
        print(f"initialize() failed, error code =", mt5.last_error())

        quit()

    timezone = pytz.timezone("Europe/Paris")
    time_from = datetime.datetime(year, month, day, tzinfo=timezone)

    time_to = datetime.datetime.now(timezone) + datetime.timedelta(days=1)

    rates = mt5.copy_rates_range(asset, time_frame, time_from, time_to)

    rates_frame = pd.DataFrame(rates)

    return rates_frame


def add_column(data: ndarray, times: int = 1):

    # for _ in range(1, times + 1):
    #     # for 0 in range(times):
    #     new = np.zeros((len(data), 1), dtype=float)
    #     data = np.append(data, new, axis=1)

    # 这不是相同的吗
    new = np.zeros((len(data), times), dtype=float)
    data = np.append(data, new, axis=1)

    return data


def delete_column(data: ndarray, index: int, times: int):
    # 这个只能连续删除
    for _ in range(1, times + 1):
        data = np.delete(data, index, axis=1)
    return data


# def delete_column(data: ndarray, index: list) -> ndarray:
#     data = np.delete(data, index, axis=1)
#     return data


def add_row(data: ndarray, times: int):
    # for _ in range(1, times + 1):
    #     columns = data.shape[1]
    #     new = np.zeros((1, columns), dtype=float)
    #     data = np.append(data, new, axis=0)

    columns = data.shape[1]
    new = np.zeros((times, columns), dtype=float)
    data = np.append(data, new, axis=0)

    return data


def delete_row(data: ndarray, number: int) -> ndarray:
    """This simple function states that the data actually starts from the `number` index and continues to the end of the `data`.

    Parameters
    ----------
    data : ndarray
        _description_
    number : int
        _description_

    Returns
    -------
    ndarray
        _description_
    """
    data = data[number:]
    return data


def rounding(data: ndarray, how_far: int = 4) -> ndarray:
    data = data.round(decimals=how_far)
    return data


def signal(data):
    data = add_column(data, 5)
    for i in range(len(data)):
        try:
            # long
            if (
                data[i, 2] < data[i - 5, 2]
                and data[i, 2] < data[i - 13, 2]
                and data[i, 2] > data[i - 21, 2]
                and data[i, 3] > data[i - 1, 3]
                and data[i, 4] == 0
            ):
                data[i + 1, 4] = 1
            elif (
                data[i, 1] > data[i - 5, 1]
                and data[i, 1] > data[i - 13, 1]
                and data[i, 1] < data[i - 21, 1]
                and data[i, 3] < data[i - 1, 3]
                and data[i, 5] == 0
            ):
                data[i + 1, 5] = -1
        except IndexError:
            pass

    return data


def signal_pd(data: DataFrame) -> DataFrame:
    long_condition_1 = (
        (data["low"] < data["low"].shift(5))
        & (data["low"] < data["low"].shift(13))
        & (data["low"] < data["low"].shift(21))
    )
    long_condition_2 = data["close"] > data["close"].shift(3)

    data["long"] = (long_condition_1 & long_condition_2).astype(int).shift(1)

    short_condition_1 = (
        (data["high"] > data["high"].shift(5))
        & (data["high"] > data["high"].shift(12))
        & (data["high"] < data["high"].shift(21))
    )
    short_condition_2 = data["close"] < data["close"].shift(3)

    data["short"] = (short_condition_1 & short_condition_2).astype(int).shift(1)

    return data


def ohlc_plot_bars(data, window):
    sample = data[-window:,]

    for i in range(len(sample)):
        plt.vlines(
            x=i, ymin=sample[i, 2], ymax=sample[i, 1], color="black", linewidth=1
        )
        if sample[i, 3] > sample[i, 0]:
            plt.vlines(
                x=i, ymin=sample[i, 0], ymax=sample[i, 3], color="black", linewidth=1
            )
        if sample[i, 3] < sample[i, 0]:
            plt.vlines(
                x=i, ymin=sample[i, 3], ymax=sample[i, 0], color="black", linewidth=1
            )
        if sample[i, 3] == sample[i, 0]:
            plt.vlines(
                x=i,
                ymin=sample[i, 3],
                ymax=sample[i, 0] + 1e-5,
                color="black",
                linewidth=1,
            )
    plt.grid()


def signal_chart(
    data, position: int, buy_column: int, sell_column: int, window: int = 500
):
    sample = data[-window:,]
    fig, ax = plt.subplots(figsize=(10, 5))
    ohlc_plot_bars(data, window)

    for i in range(len(sample)):
        x = i
        y = sample[i, position]

        if sample[i, buy_column] == 1:

            ax.annotate(
                " ",
                xy=(x, y),
                arrowprops=dict(width=9, headlength=11, headwidth=11, color="green"),
            )
        elif sample[i, sell_column] == -1:

            ax.annotate(
                " ",
                xy=(x, y),
                arrowprops=dict(width=9, headlength=-11, headwidth=-11, color="red"),
            )


def performance(
    data,
    open_price,
    buy_column,
    sell_column,
    long_result_col,
    short_result_col,
    total_result_col,
):
    for i in range(len(data)):
        try:
            # 做多收益
            if data[i, buy_column] == 1:
                for a in range(i + 1, i + 1000):
                    # 如果遇见下一个买卖信号，结算该信号的损益
                    if data[a, buy_column] == 1 or data[a, sell_column] == -1:
                        data[a, long_result_col] = (
                            data[a, open_price] - data[i, open_price]
                        )
                        break
                    else:
                        continue

            else:
                continue
        except IndexError:
            pass
    for i in range(len(data)):
        try:
            # 做空收益
            if data[i, sell_column] == -1:
                for a in range(i + 1, i + 1000):
                    if data[a, buy_column] == 1 or data[a, sell_column] == -1:
                        data[a, short_result_col] = (
                            data[i, open_price] - data[a, open_price]
                        )
                        break
                    else:
                        continue
            else:
                continue
        except IndexError:
            pass

    data[:, total_result_col] = data[:, long_result_col] + data[:, short_result_col]

    total_net_profits = data[data[:, total_result_col] > 0, total_result_col]
    total_net_losses = data[data[:, total_result_col] < 0, total_result_col]
    total_net_losses = abs(total_net_losses)

    profit_factor = round(np.sum(total_net_profits) / np.sum(total_net_losses), 2)

    trades = len(total_net_profits) + len(total_net_losses)

    # Hit ratio
    hit_ratio = 100 * len(total_net_profits) / trades

    average_gain = total_net_profits.mean()
    average_loss = total_net_losses.mean()
    realized_risk_reward = average_gain / average_loss

    print("Hit ration       = ", hit_ratio)
    print("Profit factor    = ", profit_factor)
    print("Realized RR      = ", realized_risk_reward)
    print("Number of Trades = ", trades)
    return data


if __name__ == "__main__":
    t = mass_import(0, "D1")
    t = signal(t)
    signal_chart(t, 0, 4, 5, window=250)
