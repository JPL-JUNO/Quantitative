"""
@File         : ma.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-26 12:33:12
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brute
import sys
from os import path
from pathlib import Path

plt.rcParams["savefig.dpi"] = 300

sys.path.append(path.join(path.dirname(__file__), "../../"))
from source.trend import Trend


class TAMA(Trend):
    def __init__(self, underlying, fast, slow, train_size=0.8, short=False) -> None:
        super().__init__(train_size, short)
        self.underlying = underlying
        self.fast = fast
        self.slow = slow
        self.load_data()

    def set_parameters(self, fast=None, slow=None):
        if slow:
            self.slow = slow
            self.data["SMA_slow"] = self.data["close"].rolling(self.slow).mean()
        if fast:
            self.fast = fast
            self.data["SMA_fast"] = self.data["close"].rolling(self.fast).mean()

    def load_data(self):
        raw = pd.read_csv(
            f"./data/{self.underlying}.csv", parse_dates=["date"]
        ).dropna()
        raw["returns"] = raw["close"].apply(np.log).diff()
        raw["SMA_fast"] = raw["close"].rolling(self.fast).mean()
        raw["SMA_slow"] = raw["close"].rolling(self.slow).mean()
        self.data = raw

    def backtest(self):
        data = self.data.copy().dropna()
        if self.short:
            data["position"] = np.where(data["SMA_fast"] > data["SMA_slow"], 1, -1)
        else:
            data["position"] = np.where(data["SMA_fast"] > data["SMA_slow"], 1, 0)

        data["strategy"] = data["position"].shift(1) * data["returns"]
        data.dropna(inplace=True)
        self.train_samples = int(self.train_size * len(data))
        self.train = data.iloc[: self.train_samples].copy()
        self.test = data.iloc[self.train_samples :].copy()

        self.train, aperf, operf = self.__calculate(self.train)

        self.results = self.train

        return round(aperf, 4), round(operf, 4)

    def __calculate(self, df: pd.DataFrame):
        df["buy_and_hold"] = df["returns"].cumsum().apply(np.exp)
        df["strategy_returns"] = df["strategy"].cumsum().apply(np.exp)

        aperf = df["strategy_returns"].iloc[-1]
        operf = aperf - df["buy_and_hold"].iloc[-1]
        return df, aperf, operf

    def test_backtest(self):
        self.test, aperf, operf = self.__calculate(self.test)

        return round(aperf, 4), round(operf, 4)

    def stop_loss(self):
        pass

    def keep_profit(self):
        pass

    def plot_results(self, test: bool, save=True):
        if not hasattr(self, "results"):
            raise AttributeError("No results to plot yet. Run a backtest.")
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        title = f"{self.underlying}_fast={self.fast:d}_slow={self.slow:d}_short={self.short}"
        if test:
            self.test_backtest()
        self.test[["buy_and_hold", "strategy_returns"]].plot(
            title="Test", figsize=(10, 6), ax=axes[1]
        )

        self.results[["buy_and_hold", "strategy_returns"]].plot(
            title="Train", figsize=(10, 6), ax=axes[0]
        )
        axes[0].axhline(1, color="red", linestyle=":")
        axes[1].axhline(1, color="red", linestyle=":")
        plt.suptitle(title)
        plt.tight_layout()
        if save:
            plt.savefig(f"figures/{title}.png")

    def update_and_backtest(self, parameters: tuple):
        self.set_parameters(int(parameters[0]), int(parameters[1]))
        return -self.backtest()[0]

    def optimize(self, fast_range, slow_range):
        opt = brute(self.update_and_backtest, (fast_range, slow_range), finish=None)
        return opt, -self.update_and_backtest(opt)


def get_underlying(dir):
    for underlying in Path(dir).glob("*.csv"):
        yield underlying.stem


if __name__ == "__main__":
    underlyings = get_underlying("./data")
    for underlying in underlyings:
        ma = TAMA(underlying=underlying, fast=42, slow=252)

        print(ma.backtest())

        print(ma.optimize((10, 60, 5), (180, 252, 5)))

        ma.plot_results(test=True)
