"""
@File         : reach_high.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-24 15:16:02
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from os import path
from tqdm import tqdm
import logging

sys.path.append(path.join(path.dirname(__file__), ".."))
plt.rcParams["figure.figsize"] = (18, 10)
plt.rcParams["figure.dpi"] = 300

high_periods = 30
underlying = "515220"

from utils.underlyings import get_underlying

logging.basicConfig(filename="./log/reach_high.log", level=logging.INFO)

underlyings = get_underlying("./data/")
strategy_days = range(1, 21)
logger = logging.getLogger("Reach High")


raw = pd.read_csv(f"./data/{underlying}.csv", parse_dates=["date"])
raw["reach_high"] = raw["close"].rolling(window=high_periods).max()
raw["return"] = raw["close"].apply(np.log).diff()
raw["signal"] = 0

raw["signal"] = np.where(raw["close"] == raw["reach_high"], 1, raw["signal"])
limit = raw["return"].max()

# 移除一些涨停，认为涨停是不能直接以收盘价买入的
raw["signal"] = np.where(raw["return"] > np.log(1.099), 0, raw["signal"])
data_nums = len(raw)

buy_signal = raw[raw["signal"] == 1].index
cols = []

for strategy_day in strategy_days:
    raw["adj_signal"] = 0

    for idx, signal_idx in enumerate(buy_signal):
        if idx == 0:
            for i in range(signal_idx + 1, signal_idx + strategy_day + 1):
                if i < data_nums:
                    raw.at[i, "adj_signal"] = 1
        else:
            if signal_idx < buy_signal[idx - 1] + strategy_day:
                continue
            for i in range(signal_idx + 1, signal_idx + strategy_day + 1):
                if i < data_nums:
                    raw.at[i, "adj_signal"] = 1

    raw[f"strategy_{strategy_day}"] = (
        (raw["adj_signal"] * raw["return"]).cumsum().apply(np.exp)
    )
    cols.append(f"strategy_{strategy_day}")

# raw["bh"] = raw["return"].cumsum().apply(np.exp)
strategy_returns = raw.iloc[-1][cols]
best_hold_days = strategy_days[strategy_returns.argmax()]
logger.info(
    f"{underlying!r} best hold day(s) {best_hold_days} return(s) {strategy_returns.max()}"
)
raw[cols].plot()
plt.tight_layout()
plt.savefig(f"./figures/reach_high/{high_periods}/{underlying}.png")
plt.close("all")
