"""
@File         : macd.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-07-18 22:08:38
@Email        : cuixuanstephen@gmail.com
@Description  : 移动平均线收敛发散的实现

The Moving Average Convergence Divergence
 (MACD) was developed by Gerald Appel, and is based on the differences
 between two moving averages of different lengths, a Fast and a Slow moving
 average. A second line, called the Signal line is plotted as a moving
 average of the MACD. A third line, called the MACD Histogram is
 optionally plotted as a histogram of the difference between the
 MACD and the Signal Line.

 MACD = FastMA - SlowMA

Where:

FastMA is the shorter moving average and SlowMA is the longer moving average.

SignalLine = MovAvg (MACD)

MACD Histogram = MACD - SignalLine
"""

import sys, os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))
from sources.ema import ema

import pandas as pd
import matplotlib.pyplot as plt

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

num_periods_fast = 10  # fast EMA time period

num_periods_slow = 40  # slow EMA time period

num_periods_macd = 20  # MACD EMA time period

ema_fast_values = ema(close, N=num_periods_fast)
ema_slow_values = ema(close, N=num_periods_slow)
macd_values = [fast - slow for fast, slow in zip(ema_fast_values, ema_slow_values)]

macd_signal_values = ema(macd_values, num_periods_macd)
macd_histogram_values = [
    macd - signal for macd, signal in zip(macd_values, macd_signal_values)
]

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(
    FastExponential10DayMovingAverage=pd.Series(ema_fast_values, index=goog_data.index)
)
goog_data = goog_data.assign(
    SlowExponential40DayMovingAverage=pd.Series(ema_slow_values, index=goog_data.index)
)
goog_data = goog_data.assign(
    MovingAverageConvergenceDivergence=pd.Series(macd_values, index=goog_data.index)
)
goog_data = goog_data.assign(
    Exponential20DayMovingAverageOfMACD=pd.Series(
        macd_signal_values, index=goog_data.index
    )
)
goog_data = goog_data.assign(
    MACDHistogram=pd.Series(macd_histogram_values, index=goog_data.index)
)
close_price = goog_data["ClosePrice"]
ema_f = goog_data["FastExponential10DayMovingAverage"]
ema_s = goog_data["SlowExponential40DayMovingAverage"]
macd = goog_data["MovingAverageConvergenceDivergence"]
ema_macd = goog_data["Exponential20DayMovingAverageOfMACD"]
macd_histogram = goog_data["MACDHistogram"]

fig = plt.figure()

ax1 = fig.add_subplot(311, ylabel="Google Price in $")
close_price.plot(ax=ax1, color="g", lw=2.0, legend=True)
ema_f.plot(ax=ax1, color="b", lw=2.0, legend=True)
ema_s.plot(ax=ax1, color="r", lw=2.0, legend=True)
ax2 = fig.add_subplot(312, ylabel="MACD")
macd.plot(ax=ax2, color="black", lw=2.0, legend=True)
ema_macd.plot(ax=ax2, color="g", lw=2.0, legend=True)
ax3 = fig.add_subplot(313, ylabel="MACD")
macd_histogram.plot(ax=ax3, color="r", kind="bar", legend=True, use_index=False)
ax3.set_xticks([])
plt.tight_layout()
plt.show()
