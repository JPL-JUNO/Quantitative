"""
@File         : momentum.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-07 12:00:46
@Email        : cuixuanstephen@gmail.com
@Description  : 基于动量的策略
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MomVectorBacktest(object):
    def __init__(self, symbol, start, end, amount, tc) -> None:
        self.symbol = symbol
        self.start = start
        self.end = end
        self.amount = amount
        self.tc = tc
        self.get_data()

    def get_data(self):
        raw = pd.read_csv(
            "data/aiif_eikon_eod_data.csv", index_col=0, parse_dates=True
        ).dropna()
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start : self.end]
        raw.rename(columns={self.symbol: "price"}, inplace=True)
        raw["returns"] = raw["price"].apply(np.log).diff()
        self.data = raw

    def run_strategy(self, momentum=1):
        self.momentum = momentum
        data = self.data.copy().dropna()
        data["position"] = np.sign(data["returns"].rolling(window=momentum).mean())
        data["strategy"] = data["position"].shift(1) * data["returns"]

        data.dropna(inplace=True)
        # 交易次数
        trades = data["position"].diff().fillna(0) != 0
        # data["strategy"][trades] -= self.tc
        data.loc[trades, "strategy"] -= self.tc
        data["c_returns"] = self.amount * data["returns"].cumsum().apply(np.exp)
        data["c_strategy"] = self.amount * data["strategy"].cumsum().apply(np.exp)
        self.results = data

        aperf = self.results["c_strategy"].iloc[-1]

        operf = aperf - self.results["c_returns"].iloc[-1]
        return round(aperf, 2), round(operf, 2)

    def plot_results(self):
        if not hasattr(self, "results"):
            raise AttributeError("No results to plot yet. Run a strategy.")
        title = f"{self.symbol}_TC={self.tc:.5f}"
        self.results[["c_returns", "c_strategy"]].plot(title=title, figsize=(10, 6))


if __name__ == "__main__":
    mom = MomVectorBacktest("XAU=", "2010-01-01", "2020-12-31", 10000, 0.0)

    print(mom.run_strategy())
    print(mom.run_strategy(momentum=2))
    mom = MomVectorBacktest("XAU=", "2010-1-1", "2020-12-31", 10000, 0.00025)
    print(mom.run_strategy(momentum=3))
