"""
@File         : sma.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-06 18:27:20
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import numpy as np
import pandas as pd
from scipy.optimize import brute


class SMAVectorBacktest(object):
    def __init__(self, symbol, SMA1, SMA2, start, end) -> None:
        self.symbol = symbol
        self.SMA1 = SMA1
        self.SMA2 = SMA2
        self.start = start
        self.end = end
        self.get_data()

    def get_data(self):
        raw = pd.read_csv(
            "./data/pyalgo_eikon_eod_data.csv", index_col=0, parse_dates=True
        ).dropna()
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start : self.end]
        raw.rename(columns={self.symbol: "price"}, inplace=True)
        raw["returns"] = raw["price"].apply(np.log).diff()
        raw["SMA1"] = raw["price"].rolling(self.SMA1).mean()
        raw["SMA2"] = raw["price"].rolling(self.SMA2).mean()
        self.data = raw

    def set_parameters(self, SMA1=None, SMA2=None):
        if SMA1:
            self.SMA1 = SMA1
            self.data["SMA1"] = self.data["price"].rolling(self.SMA1).mean()
        if SMA2:
            self.SMA2 = SMA2
            self.data["SMA2"] = self.data["price"].rolling(self.SMA2).mean()

    def run_strategy(self) -> tuple:
        data = self.data.copy().dropna()
        data["position"] = np.where(data["SMA1"] > data["SMA2"], 1, -1)
        data["strategy"] = data["position"].shift(1) * data["returns"]
        data.dropna(inplace=True)
        data["creturns"] = np.exp(data["returns"].cumsum())
        data["cstrategy"] = np.exp(data["strategy"].cumsum())
        self.results = data

        # gross performance of the strategy
        aperf = data["cstrategy"].iloc[-1]

        # out-/underperformance of strategy
        operf = aperf - data["creturns"].iloc[-1]
        return round(aperf, 4), round(operf, 4)

    def plot_results(self):
        if not hasattr(self, "results"):
            print("No results to plot yet. Run a strategy.")
        title = f"{self.symbol!r} | SMA1={self.SMA1:d}, SMA2={self.SMA2:d}"
        self.results[["creturns", "cstrategy"]].plot(title=title, figsize=(10, 6))

    def update_and_run(self, SMA: tuple):
        self.set_parameters(int(SMA[0]), int(SMA[1]))
        return -self.run_strategy()[0]

    def optimize_parameters(self, SMA1_range, SMA2_range):
        opt = brute(self.update_and_run, (SMA1_range, SMA2_range), finish=None)
        return opt, -self.update_and_run(opt)


if __name__ == "__main__":
    smabt = SMAVectorBacktest("EUR=", 42, 252, "2010-01-01", "2020-12-31")
    print(smabt.run_strategy())

    smabt.set_parameters(SMA1=20, SMA2=100)
    print(smabt.run_strategy())

    print(smabt.optimize_parameters((30, 56, 4), (200, 300, 4)))
