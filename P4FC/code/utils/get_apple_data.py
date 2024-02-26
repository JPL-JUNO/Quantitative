"""
@Title        : 
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2023-12-10 15:18:53
@Description  : 
"""
import pandas as pd
from pandas import DataFrame


def get_aapl(start: str = '2010-01-01', end: str = '2020-12-31', adj_close=False) -> DataFrame:
    df = pd.read_csv('../data/AAPL_20100101_20201231.csv',
                     index_col='Date', parse_dates=['Date'])
    if adj_close:
        return df.loc[start:end, ['Adj Close']]

    return df.loc[start:end]


if __name__ == '__main__':
    get_aapl()
