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
rsi_threshold = 30
rsi_timeperiod = 14
rsi = RSI(df["close"], timeperiod=rsi_timeperiod)
df["signal_rsi"] = (rsi < rsi_threshold).astype(int)

df["cost"] = 100 * df["close"] * df["signal_rsi"]  # 买入一百股
df["total_cost"] = df["cost"].cumsum()

total_market = pd.Series(np.zeros(samples_num))
for idx in df[df["signal_rsi"] == 1].index:
    if idx + 1 <= samples_num:
        current_market = (
            (df["returns"].iloc[idx + 1 :]).cumsum().apply(np.exp)
            * 100
            * df["close"].iloc[idx]
        )
        total_market = total_market.add(current_market, fill_value=0)

df["total_market"] = total_market

fig, ax = plt.subplots(3, 1, figsize=(18, 8))
df[["total_cost", "total_market"]].plot(ax=ax[0])
df["close"].plot(ax=ax[1])
long_df = df[df["signal_rsi"] == 1]
ax[2].plot(long_df["signal_rsi"], linestyle="None", marker="+")
plt.suptitle(f"Contribution Buy {underlying} via RSI {rsi_timeperiod}_{rsi_threshold}")
plt.tight_layout()

invest_cost = df["total_cost"].iloc[-1]
invest_market = df["total_market"].iloc[-1]

print(f"Current underlying: {underlying!r}")
print(f"Total cost: {invest_cost:.2f}\nTotal market: {invest_market:.2f}")
print(f"Total buy signal: {len(long_df)}")
years = round((df["date"].iloc[-1] - df["date"].iloc[0]).days / 365)
bh_annualize_returns = df["hold_returns"].iloc[-1] ** (1 / years) - 1
contribute_annualize_returns = (invest_market / invest_cost) ** (1 / years) - 1
print(f"Buy and hold annualized returns: {bh_annualize_returns:.2%}")
print(f"Contribution annualized returns: {contribute_annualize_returns:.2%}")
