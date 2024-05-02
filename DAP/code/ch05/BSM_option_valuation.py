"""
@Title        : 
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-01-11 15:04:30
@Description  : 
"""

from scipy.integrate import quad
import math
import numpy as np
import matplotlib.pyplot as plt
from typing import Union, Any

plt.rcParams['font.family'] = 'serif'


def dN(x: Union[int, float]) -> float:
    """计算标准正态分布的概率密度函数 PDF

    Parameters
    ----------
    x : Union[int, float]
        随机变量 `x`

    Returns
    -------
    float
        概率密度函数值
    """
    return math.exp(-0.5 * x ** 2) / math.sqrt(2 * math.pi)


def N(d: Union[int, float]) -> Any:
    """计算标准正态分布的累积密度函数值 CDF，用 [-20, d] 区间的值的近似
    Parameters
    ----------
    d : Union[int, float]
        随机变量

    Returns
    -------
    Any
        累积概率密度值
    """

    return quad(lambda x: dN(x), -20, d, limit=50)[0]


def BSM_call_value():
    pass


if __name__ == '__main__':
    print(N(-19))
