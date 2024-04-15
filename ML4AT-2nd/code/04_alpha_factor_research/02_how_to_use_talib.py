"""
@File         : 02_how_to_use_talib.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-11 19:36:51
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import warnings

warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from talib import RSI, BBANDS, MACD

sns.set_style("whitegrid")
idx = pd.IndexSlice

DATA_STORE = "./data/assets.h5"

with pd.HDFStore(DATA_STORE) as store:
    data = (
        store["quandl/wiki/prices"]
        .loc[
            idx["2007":"2010", "AAPL"],
            ["adj_open", "adj_high", "adj_low", "adj_close", "adj_volume"],
        ]
        .unstack("ticker")  # 多层索引，去掉 level 等于 1 的
        .swaplevel(axis=1)
        .loc[:, "AAPL"]
        .rename(columns=lambda x: x.replace("adj_", ""))
    )

up, mid, low = BBANDS(data.close, timeperiod=21, nbdevup=2, bndevdn=2, matype=0)

rsi = RSI(data.close, timeperiod=14)

macd, macdsignal, macdhist = MACD(
    data.close, fastperiod=12, slowperiod=26, signalperiod=9
)

macd_data = pd.DataFrame(
    {
        "AAPL": data.close,
        "MACD": macd,
        "MACD Signal": macdsignal,
        "MACD History": macdhist,
    }
)

fig, axes = plt.subplots(nrows=2, figsize=(15, 8), sharex=True)
macd_data.AAPL.plot(ax=axes[0])
macd_data.drop("AAPL", axis=1).plot(ax=axes[1])
fig.tight_layout()
sns.despine()

data = pd.DataFrame(
    {
        "AAPL": data.close,
        "BB Up": up,
        "BB Mid": mid,
        "BB Down": low,
        "RSI": rsi,
        "MACD": macd,
    }
)
fig, axes = plt.subplots(nrows=3, figsize=(15, 10), sharex=True)
data.drop(["RSI", "MACD"], axis=1).plot(ax=axes[0], lw=1, title="Bollinger Bands")
data["RSI"].plot(ax=axes[1], lw=1, title="Relative Strength Index")
axes[1].axhline(70, lw=1, ls="--", c="k")
axes[1].axhline(30, lw=1, ls="--", c="k")
data.MACD.plot(ax=axes[2], lw=1, title="Moving Average Convergence/Divergence", rot=0)
axes[2].set_xlabel("")
fig.tight_layout()
sns.despine()
