"""
@File         : YTM.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-25 23:42:36
@Email        : cuixuanstephen@gmail.com
@Description  : 债券收益率
"""

import numpy as np
from functools import partial
from scipy.optimize import fsolve

cash_flow = np.array([3, 3, 3, 103])
t = np.arange(0.5, 2.5, 0.5)
price = 98.39


def func(y, cash_flow, t, price):
    return np.sum(cash_flow * np.e ** (-y * t)) - price


y = fsolve(func, 0.1, args=(cash_flow, t, price))
# func = partial(func, cash_flow=cash_flow, t=t, price=price)
# y = fsolve(func, 0.1)
print(y)
