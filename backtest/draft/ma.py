import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from talib import MA

# underlying = "600036"
underlying = "512170"
slow = 20
fast = 10
df = pd.read_csv(f"./data/{underlying}.csv", parse_dates=["date"], thousands=",")
# df = df.iloc[-2000:]
samples_num = len(df)
train_size = int(samples_num * 0.8)

df["returns"] = df["close"].apply(np.log).diff()


slow_price = MA(df["close"], timeperiod=slow, matype=0)
fast_price = MA(df["close"], timeperiod=fast, matype=0)
df["fast"] = fast_price
df["slow"] = slow_price
# fig, ax = plt.subplots(3, 1, figsize=(18, 12), sharex=True)
# # ax[0].plot(df["returns"], label="returns")
# ax[0].plot(df["fast"], label="fast")
# ax[0].plot(df["slow"], label="slow")
# ax[0].legend()

# 没有做空，long 和 short
df["signal"] = (df["fast"] > df["slow"]).astype(int)

long_df = df.loc[df["signal"] == 1, :]

train = df.iloc[:train_size].copy()
test = df.iloc[train_size:].copy()

for ds in [train, test]:
    ds["strategy_returns"] = (
        (ds["signal"] * ds["returns"].shift(-1)).cumsum().apply(np.exp)
    )
    ds["hold_returns"] = ds["returns"].cumsum().apply(np.exp)

fig, axes = plt.subplots(2, 2, figsize=(18, 15))
for (idx, ax), ds in zip(enumerate(axes.T), [train, test]):
    ax[0].plot(ds["fast"], label="fast")
    ax[0].plot(ds["slow"], label="slow")
    ax[0].legend()
    ax[1].plot(ds["strategy_returns"], label="strategy_returns")
    ax[1].plot(ds["hold_returns"], label="hold_returns")
    ax[1].legend()
    ax[1].axhline(1, color="red", linestyle=":")
plt.suptitle(f"{underlying}_MA_{fast}_{slow}")
plt.tight_layout()

# df["strategy_returns"] = (df["signal"] * df["returns"].shift(-1)).cumsum().apply(np.exp)
# df["hold_returns"] = df["returns"].cumsum().apply(np.exp)
# ax[1].plot(df["strategy_returns"], label="strategy_returns")
# ax[1].plot(df["hold_returns"], label="hold_returns")
# ax[1].legend()
# ax[1].axhline(1, color="red", linestyle=":")

# # ax[2].plot(df["vol"])
# # ax[2].plot(df["returns"].rolling(window=50).sum())
# plt.suptitle(f"{underlying}_MA_{fast}_{slow}")
# plt.tight_layout()
