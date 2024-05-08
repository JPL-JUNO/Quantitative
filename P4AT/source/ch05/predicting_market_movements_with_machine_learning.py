"""
@File         : predicting_market_movements_with_machine_learning.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-07 22:28:24
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use("ggplot2")
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["figure.figsize"] = (10, 6)
os.environ["PYTHONHASHSEED"] = "0"

x = np.linspace(0, 10)


def set_seeds(seed=100):
    random.seed(seed)
    np.random.seed(seed)


set_seeds()
y = x + np.random.standard_normal(len(x))
reg = np.polyfit(x, y, deg=1)

plt.figure(figsize=(10, 6))
plt.plot(x, y, "bo", label="data")
plt.plot(x, np.polyval(reg, x), "r", lw=2.5, label="Linear Regression")
plt.legend(loc=0)

plt.figure()
plt.plot(x, y, "bo", label="data")
xn = np.linspace(0, 20)
plt.plot(xn, np.polyval(reg, xn), "r", lw=2.5, label="Linear Regression")
plt.legend(loc=0)

x = np.arange(12)
lags = 3

m = np.zeros((lags + 1, len(x) - lags))
m[lags] = x[lags:]
for i in range(lags):
    m[i] = x[i : i - lags]

reg = np.linalg.lstsq(m[:lags].T, m[lags], rcond=None)[0]

import pandas as pd

raw = pd.read_csv(
    "data/pyalgo_eikon_eod_data.csv", index_col=0, parse_dates=True
).dropna()

symbol = "EUR="
data = pd.DataFrame(raw[symbol])
data.rename(columns={symbol: "price"}, inplace=True)

lags = 5
cols = []
for lag in range(1, lags + 1):
    col = f"lag_{lag}"
    data[col] = data["price"].shift(lag)
    cols.append(col)
data.dropna(inplace=True)

reg = np.linalg.lstsq(data[cols], data["price"], rcond=None)[0]

data["prediction"] = np.dot(data[cols], reg)
data[["price", "prediction"]].plot()
