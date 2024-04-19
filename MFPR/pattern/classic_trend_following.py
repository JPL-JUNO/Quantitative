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

sys.path.append(path.normpath(path.join(path.dirname(__file__), "..")))
from pattern.financial_pattern_recognition import FinancialPatternRecognition


class ClassicTrend(FinancialPatternRecognition):
    def __init__(self) -> None:
        super().__init__()
        pass

    def marubozu(self, data: pd.DataFrame):
        signal = np.zeros(len(data))  # 初始化信号
