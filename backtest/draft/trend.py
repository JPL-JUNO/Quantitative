"""
@File         : trend.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-26 22:55:48
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from talib import MAX, MA, RSI

underlying = "600900"
df = pd.read_csv(f"./data/{underlying}.csv", parse_dates=["date"], thousands=",")
samples_num = len(df)
df["returns"] = df["close"].apply(np.log).diff()

df["cur_max"] = MAX(df["close"], timeperiod=50)
df["condition1"] = (df["close"] >= df["cur_max"]).astype(int)
df["ma_50"] = MA(df["close"], timeperiod=50, matype=0)
df["ma_100"] = MA(df["close"], timeperiod=100, matype=0)
df["condition2"] = (df["ma_50"] > df["ma_100"]).astype(int)
df["signal"] = df["condition1"] & df["condition2"]

df["strategy_returns"] = (df["signal"] * df["returns"].shift(-1)).cumsum().apply(np.exp)
df["hold_returns"] = df["returns"].cumsum().apply(np.exp)

# fig, ax = plt.subplots(2, 1, figsize=(18, 12), sharex=True)
# # ax[0].plot(df["returns"], label="returns")
# df[["close", "cur_max"]].plot(ax=ax[0])
# ax[0].legend()

# df[["strategy_returns", "hold_returns"]].plot(ax=ax[1])

rsi = RSI(df["close"], timeperiod=14)
df["signal_rsi"] = (rsi < 30).astype(int)
df['cumsum_returns'] = df['returns'][::-1].shift(1).cumsum().apply(np.exp)