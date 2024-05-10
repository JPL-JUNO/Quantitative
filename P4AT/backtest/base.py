"""
@File         : base.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-10 22:27:21
@Email        : cuixuanstephen@gmail.com
@Description  : 回测基类，实现获取和准备数据、辅助函数（绘图等）、下单和平仓
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (10, 6)


class BacktestBase:
    def __init__(
        self, symbol, start, end, amount, ftc=0.0, ptc=0.0, verbose=True
    ) -> None:
        self.symbol = symbol
        self.start = start
        self.end = end
        self.initial_amount = amount
        self.amount = amount
        self.ftc = ftc
        self.ptc = ptc
        self.units = 0
        self.position = 0
        self.trades = 0
        self.verbose = verbose
        self.get_data()

    def get_data(self):
        raw = pd.read_csv(
            "./data/pyalgo_eikon_eod_data.csv", index_col=0, parse_dates=True
        ).dropna()
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start : self.end]
        raw.rename(columns={self.symbol: "price"}, inplace=True)
        raw["return"] = raw["price"].apply(np.log).diff()
        self.data = raw

    def plot_data(self, cols=None):
        if cols is None:
            cols = ["price"]
        self.data[cols].plot(title=self.symbol)

    def get_data_price(self, bar: int) -> tuple[str, float]:
        date = str(self.data.index[bar])[:10]
        price = self.data["price"].iloc[bar]
        return date, price

    def print_balance(self, bar):
        date, _ = self.get_data_price(bar)
        print(f"{date} | current balance {self.amount:.2f}")

    def print_net_wealth(self, bar):
        date, price = self.get_data_price(bar)
        net_wealth = self.units * price + self.amount
        print(f"{date} | current net wealth {net_wealth:.2f}")

    def place_buy_order(self, bar, units=None, amount=None):
        date, price = self.get_data_price(bar)
        if units is None:
            units = int(amount / price)
        if self.amount < ((units * price) * (1 + self.ptc) + self.ftc):
            raise ValueError("账面金额不足，无法成交")
        self.amount -= (units * price) * (1 + self.ptc) + self.ftc
        self.units += units
        self.trades += 1
        if self.verbose:
            print(f"{date} | buying {units} units at {price:.3f}")
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def place_sell_order(self, bar, units, amount=None):
        date, price = self.get_data_price(bar)
        if units is None:
            units = int(amount / price)
        self.amount += (units * price) * (1 - self.ptc) - self.ftc
        self.units -= units  # 可以卖空？
        self.trades += 1
        if self.verbose:
            print(f"{date} | selling {units} units at {price:.3f}")
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def close_out(self, bar):
        date, price = self.get_data_price(bar)
        self.amount += self.units * price
        self.units = 0
        self.trades += 1
        if self.verbose:
            print(f"{date} | inventory {self.units} units at {price:.3f}")
            print("=" * 35)
        print(f"Final balance [$] {self.amount:.2f}")

        perf = (self.amount - self.initial_amount) / self.initial_amount * 100
        print(f"Net Performance [%] {perf:.2f}")
        print(f"Trades Executed [#] {self.trades:.2f}")
        print("=" * 35)


if __name__ == "__main__":
    bb = BacktestBase("AAPL.O", "2010-01-01", "2019-12-31", 10_000)
    print(bb.data.info())
    print(bb.data.tail())
    bb.plot_data()
