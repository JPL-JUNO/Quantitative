"""
@File         : sharpe_ratio.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-24 23:23:12
@Email        : cuixuanstephen@gmail.com
@Description  : 夏普比率
"""

import pandas as pd
import numpy as np

df = pd.DataFrame(
    {
        "date": pd.date_range("2013-06-20", "2023-12-31", freq="6M"),
        "rtn": np.random.rand(22) - 0.2,
    }
)

sharpe_ratio = (df["rtn"].mean() * 2 - 0.038) / (df["rtn"].std() * np.sqrt(2))

rtn_year = df.groupby(pd.Grouper(key="date", freq="Y")).sum()
sharpe_ratio_freq_year = (rtn_year["rtn"].mean() - 0.038) / rtn_year["rtn"].std()
