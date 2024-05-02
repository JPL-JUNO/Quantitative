"""
@File         : max_drawdown.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-24 23:59:16
@Email        : cuixuanstephen@gmail.com
@Description  : 最大回撤
"""

import pandas as pd
import numpy as np

# 生成一些工作日（假设为交易日）以及收益率
df = pd.DataFrame(
    {
        "trade_date": pd.date_range("2023-01-01", "2024-02-24", freq="B"),
        "rtn": np.random.standard_normal(size=300) / 100,
    }
)
# 计算累积收益率
df["cumsum"] = 1 + df["rtn"].cumsum()
df["cummax"] = df["cumsum"].cummax()
max_dropdown = np.max(1 - df["cumsum"] / df["cummax"]) * 100
print(max_dropdown)
