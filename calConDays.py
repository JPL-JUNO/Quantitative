import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

import pandas as pd


def cal_con_days(returns):
    returns = np.sign(returns)
    c_days = []
    day = 1
    sign = np.sign(returns[0])
    for i in range(0, len(returns)-1):
        if returns[i] != returns[i+1]:
            c_days.append(day * sign)
            day = 1
            sign *= -1
        else:
            day += 1
    c_days.append(day)
    return np.array(c_days)


def create_df(arr):
    c_days = pd.DataFrame({'连续天数': dict(Counter(arr)).keys(),
                           '出现次数': dict(Counter(arr)).values()})
    c_days['占比'] = (100 * c_days['出现次数'] / sum(c_days['出现次数'])).round(2).map('{}%'.format)
    c_days['涨跌'] = c_days.apply(lambda x: 'red' if x['连续天数'] > 0 else 'green', axis=1)

    return c_days


def plot(arr):
    dataframe = create_df(arr)
    plt.subplots(1, 1, figsize=(10, 10))
    p = plt.bar(dataframe.连续天数, dataframe.出现次数, color=dataframe.涨跌, alpha=.6)
    plt.bar_label(p, labels=dataframe.占比)
    plt.xticks(ticks=dataframe.连续天数)
    plt.show()


s = np.random.randn(1000)
ret = cal_con_days(s)
plot(ret)
