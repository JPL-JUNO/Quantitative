"""
@File         : mr.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-07 15:24:55
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MRVectorBacktest(object):
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

    def run_strategy(self, SMA, threshold):
        data = self.data.copy().dropna()
        data["sma"] = data["price"].rolling(SMA).mean()
        data["distance"] = data["price"] - data["sma"]
        data.dropna(inplace=True)

        # short signals
        data["position"] = np.where(data["distance"] > threshold, -1, np.nan)

        # long signals
        data["position"] = np.where(data["distance"] < -threshold, 1, data["position"])

        # crossing of current price and SMA (zero distance)
        data["position"] = np.where(
            data["distance"] * data["distance"].shift(1) < 0, 0, data["position"]
        )
        data["position"] = data["position"].ffill().fillna(0)
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
    mrbt = MRVectorBacktest("GDX", "2010-1-1", "2020-12-31", 10000, 0.0)

    print(mrbt.run_strategy(SMA=25, threshold=5))
    mrbt = MRVectorBacktest("GDX", "2010-1-1", "2020-12-31", 10000, 0.001)
    print(mrbt.run_strategy(SMA=25, threshold=5))
    mrbt = MRVectorBacktest("AAPL.O", "2010-1-1", "2020-12-31", 10000, 0.001)
    print(mrbt.run_strategy(SMA=42, threshold=10))
