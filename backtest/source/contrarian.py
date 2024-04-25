"""
@File         : contrarian.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-24 21:54:12
@Email        : cuixuanstephen@gmail.com
@Description  : 反转指标的回测
"""

import sys
from os import path

sys.path.append(path.join(path.dirname(__file__), ".."))
from source.performance.metrics import Metrics


class Contrarian:
    def __init__(self) -> None:
        self.metrics = Metrics()

    def backtest(self) -> None:
        raise NotImplementedError

    def hit_ratio(self) -> float:
        return self.metrics.hit_ratio(self.df)
