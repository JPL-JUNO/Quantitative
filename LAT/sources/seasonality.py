import pandas as pd
import matplotlib.pyplot as plt

from pandas_datareader import data

start_date = "2001-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "data/goog_data_large.pkl"

try:
    goog_data = pd.read_pickle(SRC_DATA_FILENAME)
    print("File data found...reading GOOG data")
except FileNotFoundError:
    print("File not found...downloading the GOOG data")
    goog_data = data.DataReader("GOOG", "yahoo", start_date, end_date)
    goog_data.to_pickle(SRC_DATA_FILENAME)

goog_monthly_return = (
    goog_data["Adj Close"]
    .pct_change()
    .groupby([goog_data.index.year, goog_data.index.month])
    .mean()
)

# goog_monthly_return_list = []
# for i in range(len(goog_monthly_return)):
#     goog_monthly_return_list.append(
#         (
#             {
#                 "month": goog_monthly_return.index[i][1],
#                 "monthly_return": goog_monthly_return.iloc[i],
#             }
#         )
#     )

goog_monthly_return_list = (
    goog_monthly_return.droplevel(level=0)
    .reset_index()
    .rename(columns={"Date": "month", "Adj Close": "monthly_return"})
)

goog_monthly_return_list.boxplot(column="monthly_return", by="month")

ax = plt.gca()
# labels = [item.get_text() for item in ax.get_xticklabels()]
labels = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
ax.set_xticklabels(labels)
ax.set_ylabel("GOOG return")
plt.tick_params(axis="both", which="major", labelsize=7)
plt.title("GOOG Monthly return 2001-2018")
plt.suptitle("")
plt.show()


def plot_rolling_statistics_ts(ts: pd.Series, titletext, ytext, window_size=12):
    ts.plot(color="red", label="Original", lw=0.5)
    ts.rolling(window_size).mean().plot(color="blue", label="Rolling Mean")
    ts.rolling(window_size).std().plot(color="black", label="Rolling Std")

    plt.legend()
    plt.ylabel(ytext)
    plt.title(titletext)
    plt.show(block=False)


plot_rolling_statistics_ts(
    goog_monthly_return[1:],
    "GOOG prices rolling mean sna standard deviation",
    "Monthly return ",
)
plot_rolling_statistics_ts(
    goog_data["Adj Close"],
    "GOOG prices rolling mean and standard deviation",
    "Daily prices",
    365,
)
plot_rolling_statistics_ts(
    goog_data["Adj Close"].diff(365).dropna(),
    "GOOG prices rolling mean and standard deviation",
    "Daily prices",
    365,
)

# 我们观察到，当使用每日价格而不是每日回报时，滚动平均值和滚动方差不是恒定的。
# 时间序列的非平稳性通常可以归因于两个因素：趋势和季节性。

# 增强 Dickey‑Fuller 检验
# 1. 这决定了时间序列中单位根的存在。
# 2. 如果存在单位根，则时间序列不是平稳的。
# 3. 该检验的零假设是该序列具有单位根（非平稳）。
# 4. 如果我们拒绝原假设，这意味着我们找不到单位根。
# 5. 如果我们不能拒绝原假设，我们可以说时间序列是非平稳的：

from statsmodels.tsa.stattools import adfuller


def test_stationarity(ts):
    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(ts, autolag="AIC")
    output = pd.Series(
        dftest[0:4],
        index=[
            "Test Statistic",
            "p-value",
            "#Lags Used",
            "Number of Observations Used",
        ],
    )
    print(output)


test_stationarity(goog_monthly_return[1:])
test_stationarity(goog_data["Adj Close"])

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

plt.figure()
plt.subplot(211)
plot_acf(goog_monthly_return[1:], ax=plt.gca(), lags=10)
plt.subplot(212)
plot_pacf(goog_monthly_return[1:], ax=plt.gca(), lags=10)
plt.tight_layout()
plt.show()

# 严格平稳的序列，值之间没有依赖关系。我们可以使用常规线性回归来预测值。
# 值之间存在依赖关系的序列。我们将不得不使用其他统计模型。在本章中，我们选择重点介绍使用自回归综合移
# 动平均线(ARIMA)模型。
# 1. Autoregressive (AR) term (p)—lags of dependent variables.
# Example for 3, the predictors for x(t) is x(t-1) + x(t-2) + x(t-3).
# 2. Moving average (MA) term (q)—lags for errors in prediction.
# Example for 3, the predictor for x(t) is e(t-1) + e(t-2) + e(t-3),
# where e(i) is the difference between the moving average value
# and the actual value.
# moving average?
# 3. Differentiation (d)— This is the d number of occasions where
# we apply differentiation between values

from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(goog_monthly_return[1:], order=(2, 0, 2))
fitted_results = model.fit()
goog_monthly_return[1:].plot()
fitted_results.fittedvalues.plot(color="red")
plt.show()
