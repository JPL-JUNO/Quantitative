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

plt.rcParams["figure.dpi"] = 300
plt.style.use("ggplot")


class TARSI(Contrarian):
    def __init__(self) -> None:
        super().__init__()

    def set_parameters(self, buy_threshold=30, hold_days=10, timeperiod=14):
        self.hold_days = hold_days
        self.buy_threshold = buy_threshold
        self.timeperiod = timeperiod

    def load_data(self, underlying):
        self.current_underlying = underlying
        raw = pd.read_csv(
            f"./data/{underlying}.csv", parse_dates=["date"], thousands=","
        )
        self.df = raw.copy()
        self.df["returns"] = self.df["close"].apply(np.log).diff()
        rsi = RSI(self.df["close"], self.timeperiod)
        self.df["rsi"] = rsi
        self.df["signal"] = np.where(self.df["rsi"] < self.buy_threshold, 1, 0)
        # self.df["signal"] = (self.df["rsi"] < self.buy_threshold).astype(int)

        raw["return"] = raw["close"].apply(np.log).diff()
        raw["signal_return"] = (
            raw["return"]
            .shift(-1)
            .rolling(FixedForwardWindowIndexer(window_size=self.hold_days))
            .sum()
        )
        raw["rsi"] = RSI(raw["close"], self.timeperiod)
        self.data = raw.copy()

    def filter_signal(self):
        self.df["signal_count"] = (
            self.df["signal"]
            .rolling(
                window=self.hold_days,
                min_periods=min(self.hold_days, self.timeperiod + 1),
            )
            .sum()
        )  # 避免因为第 timeperiod 至 hold_days 出现多次信号，而被 rolling 为 NaN，填充 signal_count 为 0
        # 不进行下面的填充应该也是可以的
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

        self.long_df = self.df.loc[self.df["signal"] == 1]

    def show_signal(self, save=False):
        _, ax = plt.subplots(3, 1, figsize=(18, 10), sharex=True)
        self.df[["close"]].plot(ax=ax[0])
        self.df[["rsi"]].plot(ax=ax[1])

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
            plt.savefig(f"./figures/RSI_{self.current_underlying}.png", dpi=500)

    def show_profit_and_loss(self, save=False):
        _, ax = plt.subplots(2, 1, figsize=(18, 10), sharex=True)
        colors = ["red" if val > 0 else "green" for val in self.long_df["hold_returns"]]
        self.long_df["hold_returns"].plot(kind="bar", ax=ax[0], color=colors)
        self.long_df["rsi"].plot(kind="bar", ax=ax[1], hatch="\\\\")
        ax[1].axhline(self.buy_threshold, color="red", linestyle=":")
        plt.tight_layout()
        if save:
            plt.savefig(
                f"./figures/RSI_{self.current_underlying}_hit_ratio.png", dpi=500
            )

    def backtest(self, underlying="510300"):
        if not getattr(self, "buy_threshold", None):
            print("buy_threshold 使用默认参数：30")
            self.buy_threshold = 30
        if not getattr(self, "hold_days", None):
            print("hold_days 使用默认参数：10")
            self.hold_days = 10
        if not getattr(self, "timeperiod", None):
            print("timeperiod 使用默认参数：14")
            self.timeperiod = 14
        self.load_data(underlying=underlying)
        self.filter_signal()
        self.calculate_returns()
        self.show_signal(save=True)
        self.show_profit_and_loss(save=True)

    def backtest_divergences(self):
        """回测 RSI 背离

        - 牛市背离发出买入信号。当价格创出新低，而 RSI 指数的底部比其前一次下跌的底部要高。一旦RSI 从第二次底部开始上扬，马上可以买进并且在近期底部的价格最低点的下方设置保护性止损单。如果 RSI 指数的第一次底部低于下参考线，而第二次底部高于下参考线，那么这就是一个非常强烈的买入信号。
        - 熊市背离发出卖出信号。当价格上涨创出新高，但是 RSI 的顶部却低于其前一次上涨的顶部的时候。一旦 RSI 从第二次顶部下跌就马上可以卖空，同时在最近的新高价上方设置保护性止损单。如果第一次 RSI 顶部超过了上参考线而第二次的顶部低于上参考线，那么卖出的信号就非常强烈。
        """
        raise NotImplementedError

    def backtest_rsi_level(self):
        """回测 RSI 水平

        - 当 RSI 击穿其下参考线，又回升到下参考线上方时买入。（仅实现这个）
        - 当 RSI 上升到上参考线上方，又回落到上参考线下方时卖出。
        """
        self.indicator = self.data.copy()
        self.indicator["signal"] = np.where(
            (self.df["rsi"].shift(periods=1) < self.buy_threshold)
            & (self.df["rsi"] > self.buy_threshold),
            1,
            0,
        )
        self.indicator.dropna(inplace=True)
        self.indicator.reset_index(drop=True, inplace=True)
        # 获取做多的索引
        self.long_indices = np.where(self.indicator["signal"] == 1)[0]

        self.compare_return()

    def compare_return(self):
        """比较策略的收益与买入并持有的收益"""
        self.indicator["strategy"] = (
            self.indicator["signal_return"] * self.indicator["signal"]
        )

        self.indicator["cum_bh"] = self.indicator["return"].cumsum().apply(np.exp)
        self.indicator["cum_strategy"] = (
            self.indicator["strategy"].cumsum().apply(np.exp)
        )

    def plot_results(self):
        fig, axes = plt.subplots(2, 1, figsize=(18, 10))
        self.indicator[["close"]].plot(ax=axes[0])
        self.indicator[["cum_strategy"]].plot(ax=axes[1])
        axes[0].plot(
            self.indicator.loc[self.long_indices, "close"], marker="^", linestyle="None"
        )
        plt.tight_layout()
        plt.savefig(
            f"./figures/rsi/{self.current_underlying}_{self.buy_threshold}_{self.hold_days}.png"
        )

    def stats_hit_ratio(self):
        long_df = self.indicator.loc[self.long_indices]
        hits = (long_df["signal_return"] > 0).cumsum()
        row_counts = pd.Series(range(1, len(long_df) + 1), index=long_df.index)
        self.hit_ratios = hits.div(row_counts, axis=0)
        fig, axes = plt.subplots(2, 1, figsize=(18, 10))
        axes[0].plot(self.hit_ratios, linestyle="None", marker="+")
        long_df["signal_return"].plot(ax=axes[1], kind="bar")
        plt.tight_layout()
        plt.savefig(
            f"./figures/rsi/hit_ratios/{self.current_underlying}_{self.buy_threshold}_{self.hold_days}.png"
        )


if __name__ == "__main__":
    rsi = TARSI()

    rsi.set_parameters(buy_threshold=30, hold_days=10)
    rsi.load_data(underlying="601138")
    rsi.backtest_rsi_level()
    rsi.plot_results()
    rsi.stats_hit_ratio()
    # rsi.backtest(underlying="510300")
