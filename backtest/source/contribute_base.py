"""
@File         : contribute_base.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-27 14:50:53
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path


class Contribute:
    def __init__(self) -> None:
        pass

    def load_data(self):
        self.df = pd.read_csv(
            f"./data/{self.underlying}.csv", parse_dates=["date"], thousands=","
        )
        self.df["log_returns"] = self.df["close"].apply(np.log).diff()
        self.samples_num = len(self.df)

    def set_parameters(self):
        raise NotImplementedError

    def signal(self):
        raise NotImplementedError

    def backtest(self):
        raise NotImplementedError

    def calculate_cost_and_returns(self, buy_num: int = 100):
        self.df["cost"] = buy_num * self.df["close"] * self.df["signal"]
        self.df["total_cost"] = self.df["cost"].cumsum()
        total_market = pd.Series(np.zeros(self.samples_num))
        for idx in self.df[self.df["signal"] == 1].index:
            if idx + 1 <= self.samples_num:
                current_market = (
                    (self.df["log_returns"].iloc[idx + 1 :]).cumsum().apply(np.exp)
                    * buy_num
                    * self.df["close"].iloc[idx]
                )
                total_market = total_market.add(current_market, fill_value=0)

        self.df["total_market"] = total_market

    def plot_payoff(self, save=False):
        fig, ax = plt.subplots(3, 1, figsize=(18, 8))
        self.df[["total_cost", "total_market"]].plot(ax=ax[0])
        self.df["close"].plot(ax=ax[1])
        long_df = self.df[self.df["signal"] == 1]
        ax[2].plot(long_df["signal"], linestyle="None", marker="+")
        plt.suptitle(
            f"Contribution Buy {self.underlying} via RSI {self.timeperiod}_{self.threshold}"
        )
        plt.tight_layout()
        if save:
            dir_folder = Path("./figures/contribute/")
            self.check_folder(dir_folder)
            plt.savefig(
                f"./figures/contribute/{self.underlying} via RSI {self.timeperiod}_{self.threshold}"
            )

    def check_folder(self, dir: Path):
        if not dir.exists():
            dir.mkdir(parents=True, exist_ok=True)
