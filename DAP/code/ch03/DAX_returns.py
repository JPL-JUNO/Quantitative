"""
@Title        : Analyzing DAX Index Quotes and Returns
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-01-16 21:08:48
@Description  : 
"""

from GBM_returns import do_analysis
from pandas import DataFrame
import numpy as np


def read_dax_data() -> DataFrame:
    DAX = pd.read_csv('../../data/DAX_20040930_20140930.csv',
                      index_col='Date', parse_dates=True)
    DAX = DAX.rename(columns={'Adj Close': 'index'})
    DAX['returns'] = DAX['index'].apply(np.log).diff()
    DAX['rea_var'] = 252 * np.cumsum(DAX['returns'] ** 2) / np.arange(len(DAX))
    DAX['rea_vol'] = np.sqrt(DAX['rea_var'])
    DAX = DAX.dropna()

    return DAX


def count_jumps(data: DataFrame, value: float) -> int:
    """Counts the number of return jumps as defined in size by value.

    Parameters
    ----------
    data : DataFrame
        数据
    value : float
        跳跃的阈值

    Returns
    -------
    int
        超过阈值的次数
    """
    jumps = np.sum(np.abs(data['returns']) > value)
    return jumps


if __name__ == '__main__':
    DAX = read_dax_data()
    do_analysis(DAX)
    jumps = count_jumps(DAX, .05)
    print(jumps)
