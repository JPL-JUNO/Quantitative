"""
@File         : backtest.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-11 17:17:00
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import sys
from os import path

sys.path.append(path.join(path.dirname(__file__), ".."))
from source.base import BacktestBase
from typing import Literal, Union
import numpy as np


class Backtest(BacktestBase):
    def __init__(self, underlying, bt_strategy, amount=40_000, ftc=0, ptc=2.5) -> None:
        super().__init__(underlying=underlying, amount=amount)
        self.bt_strategy = bt_strategy
        self.ftc = ftc
        self.ptc = ptc
        self.position = 0  # 是否有持仓，1 表示仓位不是空仓
        self.ta = {"SMA": self.__SMA, "MACD": self.__MACD}

    def protection(self, quote: dict) -> Literal[True, False]:
        if quote["close"] < self.stop_loss:
            return True
        else:
            return False

    def set_stop_loss(self, quote):
        # 设置止损价格
        low = quote["lowest_10"]
        close = quote["close"]
        self.stop_loss = close * 0.95 if low == close else low

    def keep_profit(self):
        pass

    def run_backtest(self):
        quotes = self.generate_quotes(self.indicator)
        for date, quote in quotes:
            date = str(date)[:10]
            current_price = quote["close"]
            signal = self.send_signal(quote)
            major = True if np.mean([s for s in signal.values()]) > 0 else False
            if major and self.position == 0:  # 信号是买入并且没有持仓
                # 首次买入
                max_units = int(self.amount[-1] / (current_price * 100)) * 100
                self.set_stop_loss(quote)  # 设置止损价格
                trade_record = {
                    "date": date,
                    "open_price": current_price,
                    "stop_loss": self.stop_loss,
                    "units": max_units,
                }
                self.send_order(direction=1, trade_params=trade_record)
                self.logger.info(
                    f"{date} buy {trade_record['units']} at price {trade_record['open_price']}"
                )

            elif major and self.position == 1:  # 已经买入并且有持仓
                # 需要判断是否止损、止盈
                if self.protection(quote):
                    self.send_order(
                        direction=-1,
                        trade_params={"close_price": current_price},
                    )
                    self.position = 0
                if self.keep_profit():
                    self.send_order(direction=-1, units=100)
                pass
            elif not major and self.position == 1:
                # 信号消失平仓
                current_units = self.trades[-1]["units"]
                self.send_order(
                    direction=-1,
                    trade_params={"close_price": current_price},
                )
                self.position = 0  # 没有持仓
                self.logger.info(
                    f"{date} sell {current_units} at price {current_price}"
                )
            elif not major and self.position == 0:
                # 没有信号，也没有持仓
                pass

    def send_signal(self, quote) -> dict[str, Literal[False, True]]:
        signal = {}
        for strategy in self.bt_strategy:
            signal[strategy] = self.ta[strategy](quote)

        return signal

    def __SMA(self, quotes: dict):
        fast, slow = quotes["SMA_fast"], quotes["SMA_slow"]
        if fast > slow:
            return True
        else:
            return False

    def __MACD(self, quotes: dict) -> bool:
        return True if quotes["delta_MACD"] > 0 else False


if __name__ == "__main__":
    bt = Backtest(underlying="515880", amount=40_000, bt_strategy=["MACD"])
    bt.run_backtest()
