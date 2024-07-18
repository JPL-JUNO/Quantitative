"""
@File         : support_and_resistance.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-07-18 00:28:33
@Email        : cuixuanstephen@gmail.com
@Description  : 使用最大值和最小值来创建支撑和阻力限值
"""

import pandas as pd
import numpy as np
from pandas_datareader import data


start_date = "2014-01-01"
end_date = "2018-01-01"

SRC_DATA_FILENAME = "./data/goog_data.pkl"
try:
    goog_data2 = pd.read_pickle(SRC_DATA_FILENAME)
    print("File data found...reading GOOG data")
except FileNotFoundError:
    print("File not found...downloading the GOOG data")
    goog_data2 = data.DataReader("GOOG", "yahoo", start_date, end_date)
    goog_data2.to_pickle(SRC_DATA_FILENAME)


goog_data = goog_data2.tail(620)

goog_data_signal = pd.DataFrame(index=goog_data.index)
goog_data_signal["price"] = goog_data["Adj Close"]

lows = goog_data["Low"]
highs = goog_data["High"]

import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google Price in $")
highs.plot(ax=ax1, color="c", lw=2.0)
lows.plot(ax=ax1, color="y", lw=2.0)
plt.hlines(
    highs.head(200).max(),
    lows.index.values[0],
    lows.index.values[-1],
    linewidth=2,
    color="g",
)
plt.hlines(
    lows.head(200).min(),
    lows.index.values[0],
    lows.index.values[-1],
    linewidth=2,
    color="r",
)
plt.axvline(linewidth=2, color="b", x=lows.index.values[200], linestyle=":")
plt.show()


def trading_support_resistance(data, bin_width=20):
    columns = [
        "sup_tol",
        "res_tol",
        "sup_count",
        "res_count",
        "sup",
        "res",
        "positions",
        "signal",
    ]
    data[columns] = pd.DataFrame(
        data=np.zeros(shape=(len(data), len(columns))), index=data.index
    )
    in_support = 0
    in_resistance = 0
    for x in range(bin_width - 1 + bin_width, len(data)):
        data_section = data[x - bin_width : x + 1]
        support_level = min(data_section["price"])
        resistance_level = max(data_section["price"])
        range_level = resistance_level - support_level
        data["res"][x] = resistance_level
        data["sup"][x] = support_level
        data["sup_tol"][x] = support_level + 0.2 * range_level
        data["res_tol"][x] = resistance_level - 0.2 * range_level

        if data["res_tol"][x] <= data["price"][x] <= data["res"][x]:
            in_resistance += 1
            data["res_count"][x] = in_resistance
        elif data["sup"][x] <= data["price"][x] <= data["sup_tol"][x]:
            in_support += 1
            data["sup_count"][x] = in_support
        else:
            in_support = 0
            in_resistance = 0

        if in_resistance > 2:
            data["signal"][x] = 1
        elif in_support > 2:
            data["signal"][x] = 0
        else:
            data["signal"][x] = data["signal"][x - 1]
    data["positions"] = data["signal"].diff()


trading_support_resistance(goog_data_signal)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google Price in $")
goog_data_signal["sup"].plot(ax=ax1, color="g", lw=2.0)
goog_data_signal["res"].plot(ax=ax1, color="b", lw=2.0)
goog_data_signal["price"].plot(ax=ax1, color="r", lw=2.0)
# 在压力位买入？
ax1.plot(
    goog_data_signal.loc[goog_data_signal["positions"] == 1.0].index,
    goog_data_signal["price"][goog_data_signal["positions"] == 1.0],
    "^",
    markersize=7,
    color="k",
    label="Buy",
)
# 在支撑位卖出？
ax1.plot(
    goog_data_signal.loc[goog_data_signal.positions == -1.0].index,
    goog_data_signal.price[goog_data_signal.positions == -1.0],
    "v",
    markersize=7,
    color="k",
    label="sell",
)
plt.legend()
plt.show()
