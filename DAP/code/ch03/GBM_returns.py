"""
@Title        : Analyzing Returns from Geometric Brownian Motion
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-01-14 22:55:08
@Description  : 
"""

from pandas import DataFrame
import math
import numpy as np
import pandas as pd
import scipy.stats as scs
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'serif'


def dN(x: float, mu: float, sigma: float) -> float:
    """Probability density function of a normal random variable x.

    Parameters
    ----------
    x : float
        normal random variable
    mu : float
        expected value
    sigma : float
        standard deviation

    Returns
    -------
    float
        value of probability density function
    """
    z = (x - mu) / sigma
    pdf = np.exp(-0.5 * z ** 2) / math.sqrt(2 * math.pi * sigma ** 2)
    return pdf


def simulate_gbm() -> DataFrame:
    S0 = 100.0
    T = 10.0
    r = .05
    vol = .2

    np.random.seed(250_000)
    gbm_dates = pd.date_range(start='2004-09-30',
                              end='2014-09-30',
                              freq='B')
    M = len(gbm_dates)
    I = 1
    dt = 1 / 252.  # 简化：固定时间间隔
    discount_factor = math.exp(-r * dt)  # 折现因子

    rand = np.random.standard_normal((M, I))  # 生成随机数

    S = np.zeros_like(rand)
    S[0] = S0
    for t in range(1, M):
        S[t] = S[t - 1] * np.exp((r - vol ** 2 / 2) *
                                 dt + vol * rand[t] * math.sqrt(dt))

    gbm = pd.DataFrame(S[:, 0], index=gbm_dates, columns=['index'])

    gbm['returns'] = np.log(gbm['index'] / gbm['index'].shift(1))
    # 可以理解为用交易日进行调整，相当于应该由 252 个交易日参与计算
    # 代码写法问题，np.arange(M) 写在后面不会触发除以 0 的问题，因为 pd.Series 会自动处理
    gbm['rea_var'] = 252 * np.cumsum(gbm['returns'] ** 2) / np.arange(M)
    gbm['rea_vol'] = np.sqrt(gbm['rea_var'])

    gbm = gbm.dropna()

    return gbm


def print_statistics(data: DataFrame) -> None:
    print('RETURN SAMPLE STATISTICS')
    print(50 * '-')
    print(f"Mean of Daily Log Returns {np.mean(data['returns']):9.6f}")
    print(f"Std of Daily Log Returns {np.std(data['returns']):9.6f}")
    print(f"Mean of Annua. Log Returns {252 * np.mean(data['returns']):9.6f}")
    print(
        f"Std of Annua. Log Returns {np.sqrt(252) * np.std(data['returns']):9.6f}")
    print(50 * '-')
    print(f"Skew of Sample Log Returns {scs.skew(data['returns']):9.6f}")
    print(f"Skew Normal Test p-value {scs.skewtest(data['returns'])[1]:9.6f}")

    print(50 * '-')
    print(f"Kurt of Sample Log Returns {scs.kurtosis(data['returns']):9.6f}")
    print(
        f"Kurt Normal Test p-value {scs.kurtosistest(data['returns'])[1]:9.6f}")
    print(50 * '-')
    print(f"Realized Volatility {data['rea_vol'].iloc[-1]:9.6f}")
    print(f"Realized Variance {data['rea_var'].iloc[-1]:9.6f}")


def quotes_returns(data: DataFrame) -> None:
    _, ax = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    data['index'].plot(ax=ax[0], grid=True)
    ax[0].set_ylabel('daily quotes')

    data['returns'].plot(ax=ax[1], grid=True)
    ax[1].set_ylabel('daily log returns')

    plt.grid(True)
    plt.tight_layout()


def return_histogram(data: DataFrame) -> None:
    _, ax = plt.subplots(1, figsize=(9, 5))
    x = np.linspace(min(data['returns']),
                    max(data['returns']), 100)
    ax.hist(np.array(data['returns']), bins=50, density=True)
    y = dN(x, np.mean(data['returns']), np.std(data['returns']))
    ax.plot(x, y, linewidth=2)
    plt.xlabel('log returns')
    plt.ylabel('frequency/probability')
    plt.grid(True)


if __name__ == '__main__':
    gbm = simulate_gbm()
    return_histogram(gbm)
