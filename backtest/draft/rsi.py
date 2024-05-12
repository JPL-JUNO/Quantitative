import pandas as pd
import matplotlib.pyplot as plt
from talib import RSI
import numpy as np
from pandas.api.indexers import FixedForwardWindowIndexer

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (18, 10)

underlying = "510300"
hold_days = 5
data = pd.read_csv(f"./data/{underlying}.csv")
data["return"] = data["close"].apply(np.log).diff()
data["rsi"] = RSI(data["close"], 14)
data.dropna(inplace=True)

data["signal"] = np.where(data["rsi"] < 25, 1, 0)
data["signal_return"] = (
    data["return"]
    .shift(-1)
    .rolling(FixedForwardWindowIndexer(window_size=hold_days))
    .sum()
)

data["strategy"] = data["signal"] * data["signal_return"]
data["cum_strategy"] = data["strategy"].cumsum().apply(np.exp)
data["cum_bh"] = data["return"].cumsum().apply(np.exp)
data.dropna(inplace=True)

print(data["cum_strategy"].iloc[-1])
print(data["signal"].value_counts())

fig, axes = plt.subplots(2, 1)
data[["cum_bh", "cum_strategy"]].plot(ax=axes[0])
plt.tight_layout()
plt.show()
