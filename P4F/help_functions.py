"""
@File         : help_functions.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-16 22:24:03
@Email        : cuixuanstephen@gmail.com
@Description  : 辅助函数
"""

import scipy.stats as scs
import numpy as np
import numpy.random as npr
import math


def print_statistics(a1, a2):
    sta1 = scs.describe(a1)
    sta2 = scs.describe(a2)
    print(f"{'statistic':>14} {'data set 1':>14} {'data set 2':>14}")
    print(45 * "-")
    print(f"{'size':>14} {sta1[0]:>14.3f} {sta2[0]:>14.3f}")
    print(f"{'min':>14} {sta1[1][0]:>14.3f} {sta2[1][0]:>14.3f}")
    print(f"{'max':>14} {sta1[1][1]:>14.3f} {sta2[1][1]:>14.3f}")
    print(f"{'mean':>14} {sta1[2]:>14.3f} {sta2[2]:>14.3f}")
    print(f"{'std':>14} {np.sqrt(sta1[3]):>14.3f} {np.sqrt(sta2[3]):>14.3f}")
    print(f"{'skew':>14} {sta1[4]:>14.3f} {sta2[4]:>14.3f}")
    print(f"{'kurtosis':>14} {sta1[5]:>14.3f} {sta2[5]:>14.3f}")


def srd_euler(x0, M: int, I: int, dt: float, kappa, theta, sigma):
    """_summary_

    Parameters
    ----------
    x0 : _type_
        期初值，例如短期利率
    M : int
        离散化所用的时间间隔数量
    I : int
        模拟路径数量
    dt : float
        以年表示的时间间隔长度
    kappa : _type_
        均值回归因子
    theta : _type_
        长期过程均值
    sigma : _type_
        恒定波动率参数

    Returns
    -------
    _type_
        _description_
    """
    xh = np.zeros((M + 1, I))
    x = np.zeros_like(xh)
    xh[0] = x0
    x[0] = x0
    for t in range(1, M + 1):
        xh[t] = (
            xh[t - 1]
            + kappa * (theta - np.maximum(xh[t - 1], 0)) * dt
            + sigma
            * np.sqrt(np.maximum(xh[t - 1], 0))
            * math.sqrt(dt)
            * npr.standard_normal(I)
        )
    x = np.maximum(xh, 0)
    return x


if __name__ == "__main__":
    pass
