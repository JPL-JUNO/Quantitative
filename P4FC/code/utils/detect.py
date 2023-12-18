"""
@Title        : 
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2023-12-16 16:21:12
@Description  : 
"""
import numpy as np


def get_hurst_exponent(ts, max_lag: int = 20) -> float:

    lags = range(2, max_lag)
    # 减去 lag 偏移量
    tau = [np.std(np.subtract(ts[lag:], ts[:-lag])) for lag in lags]
    # 多项式拟合
    hurst_exp = np.polyfit(np.log(lags), np.log(tau), 1)[0]

    return hurst_exp


if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as plt
    df = pd.read_csv('../../data/TSLA_20190101_20201231.csv',
                     parse_dates=['Date'], index_col=['Date'])
    df = df.loc['2020-01-01':'2020-12-21', 'Adj Close']

    lags = range(2, 200)
    tau = [np.std(np.subtract(df.values[lag:], df.values[:-lag]))
           for lag in lags]

    df.plot()

    fig, ax = plt.subplots()
    ax.plot(np.log(lags), np.log(tau))

    hurst_exp = np.polyfit(np.log(lags), np.log(tau), 1)[0]
