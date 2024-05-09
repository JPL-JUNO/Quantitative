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

data["return"] = data["price"].apply(np.log).diff()
data.dropna(inplace=True)
cols = []
for lag in range(1, lags + 1):
    col = f"lag_{lag}"
    data[col] = data["return"].shift(lag)
    cols.append(col)
data.dropna(inplace=True)

reg = np.linalg.lstsq(data[cols], data["return"], rcond=None)[0]
data["prediction"] = np.dot(data[cols], reg)

data[["return", "prediction"]].iloc[lags:].plot()

hits = np.sign(data["return"] * data["prediction"]).value_counts()

reg = np.linalg.lstsq(data[cols], np.sign(data["return"]), rcond=None)[0]

data["prediction"] = np.sign(np.dot(data[cols], reg))

x = np.arange(12)
lags = 3
m = np.zeros((lags + 1, len(x) - lags))
m[lags] = x[lags:]
for i in range(lags):
    m[i] = x[i : i - lags]

from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(m[:lags].T, m[lags])

lr = LinearRegression(fit_intercept=False)
lr.fit(m[:lags].T, m[lags])

hours = np.array(
    [
        0.5,
        0.75,
        1.0,
        1.25,
        1.5,
        1.75,
        1.75,
        2.0,
        2.25,
        2.5,
        2.75,
        3.0,
        3.25,
        3.5,
        4.0,
        4.25,
        4.5,
        4.75,
        5.0,
        5.5,
    ]
)
success = np.array([0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1])

from sklearn.linear_model import LogisticRegression

lg = LogisticRegression(solver="lbfgs")
hrs = hours.reshape(-1, 1)
lg.fit(hrs, success)

prob = lg.predict_proba(hrs)

symbol = "GLD"
data = pd.DataFrame(raw[symbol])

data.rename(columns={symbol: "price"}, inplace=True)
data["return"] = data["price"].apply(np.log).diff()
data.dropna(inplace=True)
lags = 3
cols = []
for lag in range(1, lags + 1):
    col = f"lag_{lag}"
    data[col] = data["return"].shift(lag)
    cols.append(col)
data.dropna(inplace=True)

from sklearn.metrics import accuracy_score

lg = LogisticRegression(C=1e7, solver="lbfgs", multi_class="auto", max_iter=1_000)
lg.fit(data[cols], np.sign(data["return"]))
data["prediction"] = lg.predict(data[cols])

hits = np.sign(
    data["return"].iloc[lags:] * data["prediction"].iloc[lags:]
).value_counts()

data["strategy"] = data["prediction"] * data["return"]
data[["return", "strategy"]].sum().apply(np.exp)
