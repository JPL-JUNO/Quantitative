"""
@File         : ema.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-14 01:29:52
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import sys
from os import path

sys.path.append(path.join(path.dirname(__file__), ".."))
from source.ta.ema import TAEMA
from pathlib import Path
from tqdm import tqdm

ema = TAEMA(fast=2, slow=5)


def get_underlying(dir, pattern="*.csv"):
    for file in Path(dir).glob(pattern=pattern):
        yield file.stem


underlyings = get_underlying("./data/", "*.csv")
for underlying in tqdm(underlyings):
    ema.load_data(underlying=underlying)
    strategy, bh = ema.backtest()

    ema.plot_results()
    hit_ratio = ema.stats_hit_ratios()

    ema.logger.info(
        f"{ema.current_underlying} & strategy={strategy} & buy_and_hold={bh} & hit ratio = {hit_ratio}"
    )
