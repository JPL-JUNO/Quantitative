"""
@File         : sma.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-07-18 14:17:41
@Email        : cuixuanstephen@gmail.com
@Description  : 简单移动平均线
"""

import pandas as pd

from pandas_datareader import data

start_date = "2014-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "./data/goog_data.pkl"

try:
    goog_data2 = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    goog_data2 = data.DataReader("GOOG", "yahoo", start_date, end_date)
    goog_data2.to_pickle(SRC_DATA_FILENAME)

goog_data = goog_data2.tail(620)

close = goog_data["Close"]

import statistics as stats

time_period = 20  # number of days over which to average
history = []  # to track a history of prices
sma_values = []  # to track simple moving average values
for close_price in close:
    history.append(close_price)
    # we remove oldest price because we only average over last time_period prices
    if len(history) > time_period:
        # 如果频繁删除第一个值，应该用更好的数据结构，双端队列
        del history[0]
    sma_values.append(stats.mean(history))

# 这一列的意义在哪里，本身不就有 Close?
goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(
    Simple20DayMovingAverage=pd.Series(sma_values, index=goog_data.index)
)
close_price = goog_data["ClosePrice"]
sma = goog_data["Simple20DayMovingAverage"]
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
close_price.plot(ax=ax1, color="g", lw=2.0, legend=True)
sma.plot(ax=ax1, color="r", lw=2.0, legend=True)
plt.show()
