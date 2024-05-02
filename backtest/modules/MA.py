"""
@File         : MA.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-23 21:30:24
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

from talib import MA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from os import path

sys.path.append(path.normpath(path.join(path.dirname(__file__), "..")))
from utils.plot import show_signal

fast = np.arange(10, 60, 10)
slow = np.arange(60, 110, 10)
# fast = [10]
# slow = [50]
from itertools import product

underlying = "510880"
df = pd.read_csv(f"./data/{underlying}.csv", parse_dates=["date"])
combinations = product(fast, slow)
for idx, (fast_period, slow_period) in enumerate(combinations):

    df["slow"] = MA(df["close"], timeperiod=slow_period, matype=0)
    df["fast"] = MA(df["close"], timeperiod=fast_period, matype=0)

    df["signal"] = (df["fast"] > df["slow"]).astype(int)
    # show_signal(df, pattern="MA", underlying=underlying)
    df["returns"] = df["close"].apply(np.log).diff()
    df["hold_returns"] = df["returns"] * df["signal"]
    df["cum_returns"] = df["hold_returns"].cumsum().apply(np.exp)
    long = df["signal"] == 1
    fig, ax = plt.subplots(3, 1, figsize=(18, 10), sharex=True)
    ax[0].plot(df["close"], label="price")
    ax[0].plot(
        df.loc[long, "close"],
        color="red",
        marker=".",
        linestyle="None",
        markersize=2,
        label="Hold",
    )
    ax[0].legend()
    ax[1].plot(df["cum_returns"], label="Cumulative Returns")
    ax[1].legend()
    min_max = [df["cum_returns"].idxmin(), df["cum_returns"].idxmax()]
    ax[1].plot(
        df.iloc[min_max]["cum_returns"], marker="*", color="red", linestyle="None"
    )
    ax[2].plot(df["fast"])
    ax[2].plot(df["slow"])
    ax[2].legend(["Fast", "Low"])
    plt.suptitle(f"{underlying} MA fast={fast_period}, slow={slow_period}")
    plt.tight_layout()
    plt.savefig(f"./figures/{underlying}_MA_{fast_period}_{slow_period}.png", dpi=500)
    plt.clf()
    if idx % 5 == 4:
        plt.close("all")
