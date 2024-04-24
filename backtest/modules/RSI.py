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

underlying = "515220"
df = pd.read_csv(f"./data/fund/{underlying}.csv", parse_dates=["date"], thousands=",")
df["returns"] = df["close"].apply(np.log).diff()
rsi = RSI(df["close"], timeperiod=5)
buy_threshold = 20
df["rsi"] = rsi
df["signal"] = (rsi < buy_threshold).astype(int)

hold_days = 10
# 如果五天内信号多次出现，不做任何操作，只有第一次出现才买入
df["signal_count"] = df["signal"].rolling(window=hold_days).sum()
df["signal_count"] = df["signal_count"].fillna(0)
df.loc[df["signal_count"] > 1, "signal"] = 0


indices = df.index[df["signal"] == 1]
for idx in indices:
    if idx + hold_days < len(df):
        df.at[idx + hold_days, "signal"] = 0

assert df.rolling(window=hold_days + 1)["signal"].sum().max() <= 1
df["hold_returns"] = (
    df["returns"]
    .rolling(FixedForwardWindowIndexer(window_size=hold_days))
    .sum()
    .shift(-1)
)
df.loc[df["signal"] != 1, "hold_returns"] = 0
df["cum_returns"] = df["hold_returns"].cumsum().apply(np.exp)
df["base_returns"] = df["returns"].cumsum().apply(np.exp)

fig, ax = plt.subplots(3, 1, figsize=(18, 10), sharex=True)
ax[0].plot(df["close"])
ax[1].plot(rsi)

ax[1].axhline(buy_threshold, color="red", linestyle=":")
long_signal = df["signal"] == 1
ax[0].plot(df.loc[long_signal, "close"], linestyle="None", marker="^")
ax[2].plot(df[["cum_returns", "base_returns"]], label="Cumulative Returns")
min_max = [df["cum_returns"].idxmin(), df["cum_returns"].idxmax()]
ax[2].plot(df.iloc[min_max]["cum_returns"], marker="*", color="red", linestyle="None")
plt.xlim(0, len(df) - 1)
plt.tight_layout()
plt.savefig(f"./figures/RSI_{underlying}.png", dpi=500)
# assert df['signal'].sum() == 21
long_df = df.loc[df["signal"] ==1]

fig, ax = plt.subplots(2, 1, sharex=True)
colors = ['red' if val > 0 else 'green' for val in long_df['hold_returns']]
long_df["hold_returns"].plot(kind="bar", ax=ax[0], color=colors)
long_df["rsi"].plot(kind="bar", ax=ax[1], hatch='\\\\')
ax[1].axhline(buy_threshold, color="red", linestyle=":")
plt.tight_layout()
plt.savefig(f"./figures/RSI_{underlying}_hit_ratio.png", dpi=500)
