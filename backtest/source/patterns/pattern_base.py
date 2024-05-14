"""
@File         : pattern_base.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-14 14:18:38
@Email        : cuixuanstephen@gmail.com
@Description  : 模式识别基类
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from talib import SMA, MACD
from configparser import ConfigParser
import logging
from datetime import date
from pathlib import Path

plt.rcParams["figure.figsize"] = (18, 10)


class PatternBase:
    def __init__(self):
        self.mkdir()
        pass

    def mkdir(self):
        self.results_path = Path("./figures/pattern/") / self.__class__.__name__
        self.logging_path = Path("./log/pattern/") / self.__class__.__name__
        self.results_path.mkdir(parents=True, exist_ok=True)
        self.logging_path.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            filename=self.logging_path / f"{date.today()}.log", level=logging.INFO
        )
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def load_data(self, underlying):
        self.current_underlying = underlying
        raw = pd.read_csv(f"./data/{underlying}.csv", parse_dates=True, thousands=",")
        self.data = raw

    def daily_returns(self):
        self.indicator["return"] = self.indicator["close"].apply(np.log).diff()

    def compare_returns(self):
        self.indicator.dropna(inplace=True)
        self.indicator.reset_index(inplace=True)
        self.indicator["strategy"] = (
            self.indicator["forward_returns"] * self.indicator["signal"]
        )
        self.indicator["cum_bh"] = self.indicator["return"].cumsum().apply(np.exp)
        self.indicator["cum_strategy"] = (
            self.indicator["strategy"].cumsum().apply(np.exp)
        )

    def plot_results(self):
        fig, axes = plt.subplots(2, 2, sharex="col")
        self.indicator[["cum_bh"]].plot(ax=axes[0, 0])
        self.indicator[["cum_strategy"]].plot(ax=axes[1, 0])
        long_indices = np.where(self.indicator["signal"] == 1)[0]
        self.long_df = self.indicator.loc[long_indices].reset_index(drop=True)
        self.long_df["hit_ratio"] = (
            (self.long_df["strategy"] > 0).cumsum().div(self.long_df.index + 1)
        )
        axes[0, 1].stem(self.long_df["strategy"])
        axes[1, 1].plot(self.long_df["hit_ratio"])
        plt.tight_layout()
        plt.savefig(
            self.results_path / f"{self.current_underlying}_{self.forward_days}.png"
        )
        plt.close("all")

    def hit_ratios(self):
        long_indices = np.where(self.indicator["signal"] == 1)[0]
        self.long_df = self.indicator.loc[long_indices].reset_index(drop=True)
        self.long_df["hit_ratio"] = (
            (self.long_df["strategy"] > 0).cumsum().div(self.long_df.index + 1)
        )
        _, axes = plt.subplots(2, 1, sharex=True)
        axes[0].stem(self.long_df["strategy"])
        axes[1].plot(self.long_df["hit_ratio"])
        plt.tight_layout()
        plt.savefig(self.results_path / f"hit_ratio_{self.current_underlying}.png")
        plt.close("all")
