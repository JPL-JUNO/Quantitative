"""
@File         : RSI.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-22 21:30:36
@Email        : cuixuanstephen@gmail.com
@Description  : RSI 回测
"""

from talib import RSI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas.api.indexers import FixedForwardWindowIndexer

underlying = "510050.SS"
df = pd.read_csv(f"./data/A/{underlying}.csv", parse_dates=["Date"], thousands=",")
df["returns"] = df["Adj Close"].apply(np.log).diff()
rsi = RSI(df["Adj Close"], timeperiod=14)
df["signal"] = (rsi < 35).astype(int)

# 如果五天内信号多次出现，不做任何操作，只有第一次出现才买入
df["signal_count"] = df["signal"].rolling(window=10).sum()
df["signal_count"] = df["signal_count"].fillna(0)
df.loc[df["signal_count"] > 1, "signal"] = 0


indices = df.index[df["signal"] == 1]
for idx in indices:
    if idx + 10 < len(df):
        df.at[idx + 10, "signal"] = 0

assert df.rolling(window=11)["signal"].sum().max() <= 1
df["hold_5_returns"] = (
    df["returns"].rolling(FixedForwardWindowIndexer(window_size=10)).sum().shift(-1)
)
df.loc[df["signal"] != 1, "hold_5_returns"] = 0
df["cum_returns"] = df["hold_5_returns"].cumsum()

fig, ax = plt.subplots(3, 1, figsize=(18, 10), sharex=True)
ax[0].plot(df["Adj Close"])
ax[1].plot(rsi)
long_signal = df["signal"] == 1
ax[0].plot(df.loc[long_signal, "Adj Close"], linestyle="None", marker="^")
ax[2].plot(df["cum_returns"], label="Cumulative Returns")
min_max = [df["cum_returns"].idxmin(), df["cum_returns"].idxmax()]
ax[2].plot(df.iloc[min_max]["cum_returns"], marker="*", color="red", linestyle="None")
plt.tight_layout()
plt.savefig(f"./figures/RSI_{underlying}.png", dpi=500)
# assert df['signal'].sum() == 21
