"""
@File         : sample_data.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-04 22:32:28
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import numpy as np
import pandas as pd

r = 0.05
sigma = 0.5


def generate_sample_data(rows: int, cols: int, freq="1min") -> pd.DataFrame:
    rows = int(rows)
    cols = int(cols)

    index = pd.date_range("2021-01-01", periods=rows, freq=freq)

    dt = (index[1] - index[0]) / pd.Timedelta(value="365D")
    columns = [f"No_{i}" for i in range(cols)]
    raw = np.exp(
        np.cumsum(
            (r - 0.5 * sigma**2) * dt
            + sigma * np.sqrt(dt) * np.random.standard_normal((rows, cols)),
            axis=0,
        )
    )

    raw = raw / raw[0] * 100

    df = pd.DataFrame(raw, index=index, columns=columns)
    return df
