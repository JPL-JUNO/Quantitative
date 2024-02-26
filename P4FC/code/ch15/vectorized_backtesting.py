"""
@Title: Vectorized backtesting with pandas
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-11-10 21:38:14
@Description: 简单策略：SMA20 > close price 就 long, otherwise close
"""

import pandas as pd
# from pandas.errors import SettingWithCopyWarning
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

df = yf.download('AAPL',
                 start='2016-01-01',
                 end='2021-12-31',
                 progress=False)

df = df[['Adj Close']]
# df.loc.__setitem__((slice(None), ('long_rtn')), value)
df.loc[:, ['log_rtn']] = df['Adj Close'].apply(np.log).diff(1)
# 这是危险的，因为无法确定是视图 view 还是副本 copy
# df.__getitem__('log_rtn').__setitem__('second', value)
# df['log_rtn'] = df['Adj Close'].apply(np.log).diff(1)
# .loc[row_indexer,col_indexer]

df.loc[:, ['sma_20']] = df['Adj Close'].rolling(window=20).mean()

df.loc[:, ['position']] = (df['Adj Close'] > df['sma_20']).astype(int)

assert sum((df['position'] == 1) & (
    df['position'].shift(1).isin([0, np.nan]))) == 56

fig, ax = plt.subplots(2, sharex=True)
df.loc['2021', ['Adj Close', 'sma_20']].plot(ax=ax[0])
df.loc['2021', 'position'].plot(ax=ax[1])
ax[0].set_title('Preview of our strategy in 2021')

df.loc[:, ['strategy_rtn']] = df['position'].shift(1) * df['log_rtn']
df.loc[:, ['strategy_rtn_cum']] = df['strategy_rtn'].cumsum().apply(np.exp)
df.loc[:, ['bh_rtn_cum']] = df['log_rtn'].cumsum().apply(np.exp)

df[['bh_rtn_cum', 'strategy_rtn_cum']].plot(title='Cumulative returns')

TRANSACTION_COST = .01
df.loc[:, ['tc']] = df['position'].diff(1).abs() * TRANSACTION_COST

df.loc[:, ['strategy_rtn_cum_tc']] = (
    df['strategy_rtn'] - df['tc']).cumsum().apply(np.exp)

STRATEGY_COLS = ['bh_rtn_cum', 'strategy_rtn_cum', 'strategy_rtn_cum_tc']
df.loc[:, STRATEGY_COLS].plot(title='Cumulative returns')
