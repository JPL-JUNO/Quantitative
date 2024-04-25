"""
@File         : rsi.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-25 16:37:35
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import sys
from os import path

sys.path.append(path.join(path.dirname(__file__), ".."))
from source.ta.rsi import TARSI

underlying = "603619"

rsi = TARSI(underlying=underlying)
rsi.set_parameters(buy_threshold=20, hold_days=10, timeperiod=5)
rsi.backtest()
print(rsi.hit_ratio())
