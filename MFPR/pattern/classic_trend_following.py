"""
@File         : classic_trend_following.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-19 23:13:55
@Email        : cuixuanstephen@gmail.com
@Description  : 经典的趋势跟踪
"""

import sys
from os import path
import numpy as np
import pandas as pd
import inspect

sys.path.append(path.normpath(path.join(path.dirname(__file__), "..")))
from pattern.financial_pattern_recognition import FinancialPatternRecognition


class ClassicTrend(FinancialPatternRecognition):
    def __init__(self) -> None:
        super().__init__()
        pass

    def marubozu(self, data: pd.DataFrame):
        self.pattern = inspect.currentframe().f_code.co_name
        signal = np.zeros(len(data))  # 初始化信号

    def three_candles_pd(self, data: pd.DataFrame, body=0.01) -> np.ndarray:
        self.pattern = inspect.currentframe().f_code.co_name
        rolled = data.rolling(window=4)
        signal = np.zeros(len(data))
        for idx, df in enumerate(rolled):
            if idx < 3:
                continue
            body_mask = all(((df["Close"] - df["Open"]).abs() > body).iloc[-3:])
            mask_up = all(df["Close"].diff().dropna() > 0)
            if body_mask and mask_up:
                signal[idx] = 1  # call 信号
                continue
            mask_down = all(df["Close"].diff().dropna() < 0)
            if body_mask and mask_down:
                signal[idx] = -1  # short 信号
        return signal

    def tasuki(self, data: pd.DataFrame) -> np.ndarray:
        self.pattern = inspect.currentframe().f_code.co_name
        rolled = data.rolling(window=3)

        signal = np.zeros(len(data))
        up_down = pd.Series([True, True, False])
        for idx, df in enumerate(rolled):
            if idx < 2:
                continue
            # 前两个应该是阳线，第三个是阴线
            up_down.index = df.index
            mask1_up = (df["Close"] > df["Open"]).equals(up_down)  # 基于索引的比较
            gap = df["Open"].iloc[1] > df["Close"].iloc[0]  # 跳开（多）
            mask2_up = df["Close"].iloc[0] < df["Close"].iloc[2] < df["Open"].iloc[1]
            if mask1_up and gap and mask2_up:
                signal[idx] = 1
                continue
            # 阴线、阴线、阳线
            mask1_down = (df["Close"] < df["Open"]).equals(up_down)
            gap_down = df["Open"].iloc[1] < df["Close"].iloc[0]  # 跳开（空）
            mask2_down = df["Open"].iloc[1] < df["Close"].iloc[2] < df["Close"].iloc[0]
            if mask1_down and gap_down and mask2_down:
                signal[idx] = -1

        return signal


if __name__ == "__main__":
    underlying = "CSI300"
    df = pd.read_csv(f"./data/A/{underlying}.csv", parse_dates=["Date"], thousands=",")
    df = df.rename({"Price": "Close"}, axis=1)
    df = df.sort_values(by="Date", ascending=True, ignore_index=True)
    trend = ClassicTrend()
    df["signal"] = trend.tasuki(df)
    trend.show_signal(df, underlying=underlying)
