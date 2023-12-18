"""
@Title        : 
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2023-12-14 20:46:28
@Description  : 
"""


import pandas as pd
from pandas import Series, DataFrame


def identify_outliers(df: DataFrame, column: str,
                      window_size: int = 21, n_sigmas: int = 3) -> Series:
    df = df[column].copy()

    df_rolling = df.rolling(window=window_size).agg(['mean', 'std'])
    df = df.join(df_rolling)
    df['upper'] = df['mean'] + n_sigmas * df['std']
    df['lower'] = df['mean'] - n_sigmas * df['std']

    return ((df[column] > df['upper']) | (df[column] < df['lower']))
