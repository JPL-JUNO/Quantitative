"""
@File         : rsi.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-27 14:49:12
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

from talib import RSI
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from os import path

sys.path.append(path.normpath(path.join(path.dirname(__file__), "..")))

from source.contribute_base import Contribute


class ContributeRSI(Contribute):
    def __init__(self, underlying) -> None:
        super().__init__()
        self.underlying = underlying

    def set_parameters(self, threshold=30, timeperiod=14):
        self.threshold = threshold
        self.timeperiod = timeperiod

    def signal(self):
        rsi = RSI(self.df["close"], timeperiod=self.timeperiod)
        self.df["signal"] = (rsi < self.threshold).astype(int)

    def backtest(self):
        self.set_parameters()
        self.load_data()
        self.signal()
        self.calculate_cost_and_returns()
        self.plot_payoff(save=True)


if __name__ == "__main__":
    underlying = "600900"
    con = ContributeRSI(underlying=underlying)
    con.backtest()
