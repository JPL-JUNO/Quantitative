"""
@File         : modern_trend_following_patterns.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-21 21:30:54
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import sys
from os import path
import numpy as np
import pandas as pd
import inspect

sys.path.append(path.normpath(path.join(path.dirname(__file__), "..")))
from pattern.financial_pattern_recognition import FinancialPatternRecognition


class ModernTrend(FinancialPatternRecognition):
    def __init__(self) -> None:
        super().__init__()
        pass

    def quintuplets(self, data: pd.DataFrame, max_body=0.1) -> np.ndarray:
        self.pattern = inspect.currentframe().f_code.co_name

        rolled = data.rolling(window=5)
        signal = np.zeros(len(data))
        for idx, df in enumerate(rolled):
            if idx < 4:
                continue
            # 满足不断上涨
            up = all(df["Close"].diff(periods=1).dropna() > 0)
            mask1 = all(df["Close"] > df["Open"])  # 连续的阳线
            mask2 = all((df["Close"] - df["Open"]).abs() < max_body)  # 箱体要小
            if up and mask1 and mask2:
                signal[idx] = 1
                continue
            down = all(df["Close"].diff(periods=1).dropna() < 0)
            mask1 = all(df["Close"] < df["Open"])
            if down and mask1 and mask2:
                signal[idx] = -1
        return signal


if __name__ == "__main__":
    underlying = "510880.SS"
    df = pd.read_csv(f"./data/A/{underlying}.csv", parse_dates=["Date"], thousands=",")
    # df = df.rename({"Price": "Close"}, axis=1)
    df = df.drop("Close", axis=1).rename({"Adj Close": "Close"}, axis=1)
    # df = df.rename({"Price": "Close"}, axis=1)
    df = df.sort_values(by="Date", ascending=True, ignore_index=True)
    mt = ModernTrend()
    signal = mt.quintuplets(df)
    df["signal"] = signal
    mt.show_signal(df, underlying=underlying)
