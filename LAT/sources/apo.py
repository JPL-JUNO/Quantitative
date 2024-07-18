"""
@File         : apo.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-07-18 16:28:34
@Email        : cuixuanstephen@gmail.com
@Description  : 绝对价格振荡器
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

"""
The Absolute Price Oscillator (APO) is based
 on the absolute differences between two moving averages of different
 lengths, a ‘Fast’ and a ‘Slow’ moving average.

APO = Fast Exponential Moving Average - Slow Exponential Moving Average
"""

ema_fast_values = ema(close, N=10)
ema_slow_values = ema(close, N=40)
apo_values = [fast - slow for fast, slow in zip(ema_fast_values, ema_slow_values)]

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(
    FastExponential10DayMovingAverage=pd.Series(ema_fast_values, index=goog_data.index)
)
goog_data = goog_data.assign(
    SlowExponential40DayMovingAverage=pd.Series(ema_slow_values, index=goog_data.index)
)
goog_data = goog_data.assign(
    AbsolutePriceOscillator=pd.Series(apo_values, index=goog_data.index)
)

close_price = goog_data["ClosePrice"]
ema_f = goog_data["FastExponential10DayMovingAverage"]
ema_s = goog_data["SlowExponential40DayMovingAverage"]
apo = goog_data["AbsolutePriceOscillator"]

fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel="Google Price in $")
close_price.plot(ax=ax1, color="g", lw=2.0, legend=True)
ema_f.plot(ax=ax1, color="b", lw=2.0, legend=True)
ema_s.plot(ax=ax1, color="r", lw=2.0, legend=True)
ax2 = fig.add_subplot(212, ylabel="APO")
apo.plot(ax=ax2, color="black", lw=2.0, legend=True)
plt.tight_layout()
plt.savefig("./img/apo.png")
plt.show()
