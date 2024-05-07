"""
@File         : mastering_vectorized_backtesting.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-06 15:31:44
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
import numpy as np

np.diff(prepend=np.nan)
raw = pd.read_csv(
    "data/aiif_eikon_eod_data.csv", index_col=0, parse_dates=True
).dropna()
