"""
@File         : classic.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-14 21:43:21
@Email        : cuixuanstephen@gmail.com
@Description  : 
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

sys.path.append(path.join(path.dirname(__file__), "../../../"))
from source.patterns.pattern_base import PatternBase


class Hammer(PatternBase):
    def __init__(self):
        super().__init__()

    def signal_logic(self):
        self.indicator = self.data.copy()

        grp = self.indicator.rolling(window=3)
        signal = pd.Series(np.zeros(len(self.indicator)), dtype=int)
        for idx, data in enumerate(grp):
            if idx < 2:
                continue
            k1, k2, k3, *_ = data.values
            cond1 = k1[1] > k1[4]
            cond2 = (
                k2[2] == k2[4]
                and k2[4] > k2[1]
                and (k2[4] - k2[1]) < 2 * (k2[1] - k2[3])
            )
            cond3 = k3[4] > k3[1]
            if all([cond1, cond2, cond3]):
                signal[idx] = 1

        self.indicator["signal"] = signal


if __name__ == "__main__":
    hammer = Hammer()
    hammer.load_data(underlying="603619")
    hammer.signal_logic()
    hammer.forward_returns()
    print(hammer.indicator.signal.value_counts())
