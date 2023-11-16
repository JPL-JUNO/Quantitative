"""
@Title: 
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-11-12 21:36:28
@Description: 
"""

import yfinance as yf
import numpy as np
# import matplotlib.pyplot as plt
# plt.style.use('ggplot')
# ^GSPC 是标普 500
df = yf.download(['AAPL', 'MSFT', '^GSPC'],
                 start='2010-01-01',
                 end='2018-06-29',
                 progress=False)
df = df.loc[:, ('Adj Close')]
df.plot(subplots=True)

aapl = df[['AAPL']]

df.describe().round(decimals=2)

# 增量
df.diff(periods=1)

df.pct_change(periods=1)

df.pct_change(periods=1).mean().plot(kind='bar')

rtn = (df / df.shift(periods=1)).apply(np.log)
# 当初的一块钱，现在多少钱，
rtn.cumsum().apply(np.exp)


# 重采样
df.resample('1w').last()
# label 表示重采样的时间段，左短点作为 label 还是右端点作为 label
df.resample('1w', label='left').last()

# 时间窗口
df.rolling(window=5).min()


aapl.loc[:, ['sma_5']] = aapl['AAPL'].rolling(window=5).mean()
aapl.loc[:, ['sma_20']] = aapl['AAPL'].rolling(window=20).mean()

aapl.loc[:, ['position']] = np.where(aapl['sma_5'] > aapl['sma_20'], 1, -1)

aapl.plot(secondary_y='position')
