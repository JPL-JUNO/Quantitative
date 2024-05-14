"""
@File         : trend.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-24 21:54:26
@Email        : cuixuanstephen@gmail.com
@Description  : 趋势指标回测
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["savefig.dpi"] = 300
plt.rcParams["figure.dpi"] = 300
plt.rcParams["figure.figsize"] = (18, 10)
plt.style.use("ggplot")


class Trend:
    def __init__(self, train_size: float = 0.8, short=False) -> None:
        self.train_size = train_size
        self.short = short

    def load_data(self, underlying):
        self.current_underlying = underlying
        raw = pd.read_csv(
            f"./data/{underlying}.csv", parse_dates=["date"], thousands=","
        )
        self.data = raw.copy()

    def backtest(self):
        self.calculate_returns()
        self.signal_logic()
        self.strategy_returns()
        strategy, bh = self.compare_returns()
        return strategy, bh

    def test_backtest(self):
        raise NotImplementedError

    def plot_results(self):
        self.indicator[["cum_bh", "cum_strategy"]].plot()
        plt.savefig(self.results_path / f"{self.current_underlying}.png")
        plt.close("all")

    def calculate_returns(self):
        raise NotImplementedError

    def signal_logic(self):
        raise NotImplementedError

    def strategy_returns(self):
        raise NotImplementedError

    def compare_returns(self):
        raise NotImplementedError

    def get_long_data(self):
        self.long_indices = np.where(self.indicator["signal"] == 1)[0]
        self.long_df = self.indicator.iloc[self.long_indices]
