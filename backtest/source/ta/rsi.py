"""
@File         : rsi.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-24 21:55:39
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
import numpy as np
from pandas.api.indexers import FixedForwardWindowIndexer
from talib import RSI
import matplotlib.pyplot as plt
from source.contrarian import Contrarian


class TARSI(Contrarian):
    def __init__(self, underlying) -> None:
        self.underlying = underlying

    def set_parameters(self, buy_threshold, hold_days, timeperiod=5):
        self.hold_days = hold_days
        self.buy_threshold = buy_threshold
        self.timeperiod = timeperiod

    def load_data(self):
        self.df = pd.read_csv(
            f"./data/{self.underlying}.csv", parse_dates=["date"], thousands=","
        )
        self.df["returns"] = self.df["close"].apply(np.log).diff()
        rsi = RSI(self.df["close"], self.timeperiod)
        self.df["rsi"] = rsi
        self.df["signal"] = (self.df["rsi"] < self.buy_threshold).astype(int)

    def filter_signal(self):
        self.df["signal_count"] = self.df["signal"].rolling(window=self.hold_days).sum()
        self.df["signal_count"] = self.df["signal_count"].fillna(0)
        # 如果持有期内多次出现信号，不进行任何的操作，信号保持为 0
        self.df.loc[self.df["signal_count"] > 1, "signal"] = 0

        # 保证持有期结束的那天，不应该出现 long 的信号，即使是机会，也跳过
        # 当然也可以平之前仓位，再开仓
        indices = self.df.index[self.df["signal"] == 1]

        for idx in indices:
            if idx + self.hold_days < len(self.df):
                self.df.at[idx + self.hold_days, "signal"] = 0
        # 保证持有期内，最多一次开仓

        assert (
            self.df.rolling(window=self.hold_days + 1)["signal"].sum().max() <= 1
        ), ValueError("存在持仓期内多次开仓信号")

        self.long_df = self.df.loc[self.df["signal"] == 1]

    def calculate_returns(self):
        self.df["hold_returns"] = (
            self.df["returns"]
            .rolling(FixedForwardWindowIndexer(window_size=self.hold_days))
            .sum()
            .shift(-1)
        )

        self.df.loc[self.df["signal"] != 1, "hold_returns"] = 0
        self.df["cum_returns"] = self.df["hold_returns"].cumsum().apply(np.exp)

        # 基线策略，买入并持有
        self.df["base_returns"] = self.df["returns"].cumsum().apply(np.exp)

    def show_signal(self, save=False):
        _, ax = plt.subplots(3, 1, figsize=(18, 10), sharex=True)
        ax[0].plot(self.df["close"])
        ax[1].plot(self.df["rsi"])

        ax[1].axhline(self.buy_threshold, color="red", linestyle=":")
        ax[0].plot(self.long_df["close"], linestyle="None", marker="^")
        ax[2].plot(self.df[["cum_returns", "base_returns"]], label="Cumulative Returns")
        min_max = [self.df["cum_returns"].idxmin(), self.df["cum_returns"].idxmax()]
        ax[2].plot(
            self.df.iloc[min_max]["cum_returns"],
            marker="*",
            color="red",
            linestyle="None",
        )
        plt.xlim(0, len(self.df) - 1)
        plt.tight_layout()
        if save:
            plt.savefig(f"./figures/RSI_{self.underlying}.png", dpi=500)

    def show_profit_and_loss(self, save=False):
        _, ax = plt.subplots(2, 1, sharex=True)
        colors = ["red" if val > 0 else "green" for val in self.long_df["hold_returns"]]
        self.long_df["hold_returns"].plot(kind="bar", ax=ax[0], color=colors)
        self.long_df["rsi"].plot(kind="bar", ax=ax[1], hatch="\\\\")
        ax[1].axhline(self.buy_threshold, color="red", linestyle=":")
        plt.tight_layout()
        if save:
            plt.savefig(f"./figures/RSI_{self.underlying}_hit_ratio.png", dpi=500)

    def backtest(self):
        if not getattr(self, "buy_threshold", None):
            print("buy_threshold 使用默认参数：20")
            self.buy_threshold = 5
        if not getattr(self, "hold_days", None):
            print("hold_days 使用默认参数：10")
            self.hold_days = 10
        if not getattr(self, "timeperiod", None):
            print("timeperiod 使用默认参数：5")
            self.timeperiod = 5
        self.load_data()
        self.calculate_returns()
        self.filter_signal()
        self.show_signal(save=True)
        self.show_profit_and_loss(save=True)
