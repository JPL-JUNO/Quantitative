"""
@File         : metrics.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-25 22:47:30
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import sys
from os import path

sys.path.append(path.join(path.dirname(__file__), ".."))
from source.performance.hit_ratio import hit_ratio


class Metrics:
    def __init__(self) -> None:
        pass

    def hit_ratio(self, data):
        return hit_ratio(data)
