import pandas as pd

from pandas_datareader import data

start_date = "2014-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "data/goog_data.pkl"

try:
    goog_data2 = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    goog_data2 = data.DataReader("GOOG", "yahoo", start_date, end_date)
    goog_data2.to_pickle(SRC_DATA_FILENAME)

goog_data = goog_data2.tail(620)

close = goog_data["Adj Close"]

time_period = 20
history = []
mom_values = []

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:
        del history[0]
    mom = close_price - history[0]
    mom_values.append(mom)

goog_data = goog_data.assign(
    ClosePrice=pd.Series(close, index=goog_data.index),
    MomentumFromPrice20DaysAgo=pd.Series(mom_values, index=goog_data.index),
)
close_price = goog_data["ClosePrice"]
mom = goog_data["MomentumFromPrice20DaysAgo"]

import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel="Google Price in $")
close_price.plot(ax=ax1, color="g", lw=2.0, legend=True)
ax2 = fig.add_subplot(212, ylabel="Momentum in $")
mom.plot(ax=ax2, color="b", lw=2.0, legend=True)
plt.tight_layout()
plt.show()
