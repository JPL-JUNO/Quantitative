"""
@File         : convert_choice_data.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-23 20:46:16
@Email        : cuixuanstephen@gmail.com
@Description  : 转化 choice 终端下载的数据
"""

import pandas as pd
from pathlib import Path


def get_paths(dir, pattern):
    for file in Path(dir).rglob(pattern=pattern):
        yield file, file.name


paths = get_paths("./data/source_data", "*.xls")
for path, file_name in paths:
    df = pd.read_excel(path, parse_dates=["交易时间"])
    underlying = file_name.split("_")[1]
    df = df.drop(
        labels=[
            "证券代码",
            "证券名称",
            "涨跌",
            "涨跌幅%",
        ],
        axis=1,
    )
    df = df.dropna(axis=0)
    df = df.rename(
        {
            "交易时间": "date",
            "开盘价": "open",
            "最高价": "high",
            "最低价": "low",
            "收盘价": "close",
            "成交量": "volume",
            "成交额": "amount",
        },
        axis=1,
    )
    df.to_csv(path.parent.parent / (underlying + ".csv"), index=False)
