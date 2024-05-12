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
import matplotlib.pyplot as plt

sys.path.append(path.join(path.dirname(__file__), ".."))
from source.ta.rsi import TARSI
from pathlib import Path

underlying = "513500"

rsi = TARSI()
rsi.set_parameters(buy_threshold=30, hold_days=10)


def get_underlying(dir, pattern="*.csv"):
    for file in Path(dir).glob(pattern=pattern):
        yield file.stem


# underlyings = get_underlying("./data/", "*.csv")
# for underlying in underlyings:
#     rsi.load_data(underlying=underlying)
#     rsi.backtest_rsi_level()
#     rsi.plot_results()
#     rsi.stats_hit_ratio()
#     print(
#         underlying,
#         round(rsi.indicator["cum_strategy"].iloc[-1], 2),
#         len(rsi.long_indices),
#         round(rsi.hit_ratios.iloc[-1], 2),
#         sep="&",
#     )
#     plt.close("all")

underlying = "603619"
# rsi.set_parameters(buy_threshold=30, hold_days=5)
rsi.load_data(underlying=underlying)
rsi.backtest_rsi_level()
rsi.plot_results()
rsi.stats_hit_ratio()
print(
    underlying,
    round(rsi.indicator["cum_strategy"].iloc[-1], 2),
    len(rsi.long_indices),
    round(rsi.hit_ratios.iloc[-1], 2),
    sep=" & ",
)
