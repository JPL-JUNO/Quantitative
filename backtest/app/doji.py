"""
@File         : doji.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-18 15:54:18
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import sys
from os import path
from tqdm import tqdm

sys.path.append(path.join(path.dirname(__file__), ".."))
from utils.underlyings import get_underlying
from source.patterns.contrarian.classic import Doji

doji = Doji()
underlyings = get_underlying("./data", "*.csv")
doji.logger.info("underlying & returns & hit_ratio & signals \\")
for underlying in tqdm(underlyings):
    doji.load_data(underlying=underlying)
    doji.signal_logic()
    doji.forward_returns()
    strategy_returns, bh_returns = doji.compare_returns()
    doji.plot_results()
    hit_ratio, signals = doji.hit_ratios()
    doji.logger.info(
        f"{doji.current_underlying} & {round(strategy_returns,2)} &{round(hit_ratio,2)} &{signals}\\"
    )
