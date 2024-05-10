"""
@File         : long.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-10 23:17:00
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import sys
from os import path

sys.path.append(path.join(path.dirname(__file__), ".."))

from backtest.base import BacktestBase


class BacktestLong(BacktestBase):
    def __init__(self, symbol, start, end, amount, ftc=0, ptc=0, verbose=True) -> None:
        super().__init__(symbol, start, end, amount, ftc, ptc, verbose)

    def run_mean_reversion_strategy(self, SMA, threshold):
        msg = f"""
        \n\nRunning mean reversion strategy
        SMA={SMA}, threshold={threshold}
        fixed_costs={self.ftc}, proportional_costs={self.ptc}
        """
        print(msg)
        print("=" * 35)

        self.data["SMA"] = self.data["price"].rolling(SMA).mean()
        for bar in range(SMA, len(self.data)):
            if self.position == 0:
                if (
                    self.data["price"].iloc[bar]
                    < self.data["SMA"].iloc[bar] - threshold
                ):
                    self.place_buy_order(bar, amount=self.amount)
                    self.position = 1
            elif self.position == 1:
                if self.data["price"].iloc[bar] >= self.data["SMA"].iloc[bar]:
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0
        self.close_out(bar)


if __name__ == "__main__":
    long = BacktestLong("AAPL.O", "2010-1-1", "2019-12-31", 10000, verbose=False)
    long.run_mean_reversion_strategy(50, 5)
