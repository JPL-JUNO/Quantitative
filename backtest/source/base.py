"""
@File         : base.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-11 11:29:40
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from talib import SMA, MACD
from configparser import ConfigParser
import logging
from datetime import date
from pathlib import Path

plt.rcParams["figure.figsize"] = (18, 10)


class BacktestBase:
    def __init__(
        self, underlying, amount=40_000, config_file="./config/ta_params.ini"
    ) -> None:
        self.underlying = underlying
        self.amount = [amount]
        self.parser = ConfigParser()
        self.parser.read(config_file, encoding="utf-8")

        self.log_filename = f"./log/{date.today()}.log"
        logging.basicConfig(filename=self.log_filename, level=logging.INFO)

        self.logger = logging.getLogger("backtest_logger")

        self.read_data()
        self.prepare_indicator()

        self.trades = []

    def read_data(self):
        raw = pd.read_csv(
            f"./data/{self.underlying}.csv", parse_dates=True, index_col=0
        )
        self.data = raw

    def prepare_indicator(self):
        self.indicator = self.data.copy()

        self.indicator["lowest_10"] = (
            self.indicator["close"]
            .rolling(self.parser.getint("protection", "low_periods"))
            .min()
        )

        self.indicator["SMA_fast"] = SMA(
            self.indicator["close"],
            timeperiod=self.parser.getint("overlap_studies", "SMA_fast"),
        )

        self.indicator["SMA_slow"] = SMA(
            self.indicator["close"],
            timeperiod=self.parser.getint("overlap_studies", "SMA_slow"),
        )

        (
            self.indicator["MACD"],
            self.indicator["MACD_signal"],
            self.indicator["MACD_hist"],
        ) = MACD(
            self.indicator["close"],
            fastperiod=self.parser.getint("momentum", "MACD_fast"),
            slowperiod=self.parser.getint("momentum", "MACD_slow"),
            signalperiod=self.parser.getint("momentum", "MACD_signal"),
        )
        self.indicator["delta_MACD"] = self.indicator["MACD_hist"].diff()

        self.indicator.dropna(inplace=True)

    def generate_quotes(self, df: pd.DataFrame):
        for date, quotes in df.iterrows():
            yield date, quotes.to_dict()

    def send_order(self, direction, trade_params: dict):
        if direction == 1:
            self.trades.append(trade_params)
            self.position = 1
            self.units = trade_params["units"]
        elif direction == -1:
            # ENHANCED:现在确定卖出数量为持仓的全部
            sell_units = trade_params.get("units")
            position_units = self.trades[-1]["units"]
            close_price = trade_params["close_price"]
            open_price = self.trades[-1]["open_price"]

            self.trades[-1]["close_price"] = close_price

            self.amount.append(position_units * close_price)
        else:
            raise ValueError(f"不支持的交易方向，-1 卖出，1 买入，got {direction}")


if __name__ == "__main__":
    bt = BacktestBase("515880")
    bt.send_order(direction=1)
