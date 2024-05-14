"""
@File         : kangaroo_tails.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-14 11:31:34
@Email        : cuixuanstephen@gmail.com
@Description  : 袋鼠尾模式识别
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from os import path
from pathlib import Path
from tqdm import tqdm
from pandas.api.indexers import FixedForwardWindowIndexer

plt.rcParams["savefig.dpi"] = 300
plt.rcParams["figure.dpi"] = 300
plt.rcParams["figure.figsize"] = (26, 16)
plt.style.use("ggplot")

sys.path.append(path.join(path.dirname(__file__), "../../"))
from source.patterns.pattern_base import PatternBase
from talib import EMA
import logging


class KangarooTails(PatternBase):
    def __init__(self) -> None:
        self.mkdir()

    def signal_logic(self):
        indicator = self.data.copy()
        grp = indicator.rolling(window=3, min_periods=3)
        # 阴线、阴线、阳线
        true_up_and_down = np.array([False, False, False])
        signal = pd.Series(np.zeros(len(indicator)), dtype=int)
        for idx, meta in enumerate(grp):
            if idx < 3:
                continue
            up_and_down = meta["open"] < meta["close"]
            condition1 = np.array_equal(up_and_down.values, true_up_and_down)
            _, o, h, l, c, *_ = meta.iloc[-1]
            condition2 = (c - l) > 2.5 * (o - c) > 0
            if condition1 and condition2:
                signal[idx] = 1
        indicator["signal"] = signal
        self.indicator = indicator

    def forward_returns(self, forward_days: int = 3):
        self.forward_days = forward_days
        self.daily_returns()
        self.indicator["forward_returns"] = (
            self.indicator["return"]
            .shift(-1)
            .rolling(FixedForwardWindowIndexer(window_size=forward_days))
            .sum()
        )


if __name__ == "__main__":
    kt = KangarooTails()
    for underlying in tqdm(["159985", "159980", "515220", "510880"]):
        kt.load_data(underlying=underlying)
        for forward_day in tqdm(range(2, 10)):
            kt.signal_logic()
            kt.forward_returns(forward_days=forward_day)
            kt.compare_returns()
            # kt.indicator["cum_strategy"].plot()
            kt.plot_results()
    # kt.hit_ratios()
