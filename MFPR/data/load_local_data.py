"""
@File         : load_local_data.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-16 21:22:41
@Email        : cuixuanstephen@gmail.com
@Description  : 加载本地数据
"""

import pandas as pd
import numpy as np


def load_data(asset) -> np.ndarray:
    df = pd.read_csv(f"./data/{asset}.csv")
    data = df.iloc[:, 1:5].values
    data = data.round(decimals=6)
    return data
