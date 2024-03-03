"""
@File         : 7_interactive_financial_analytics_with_the_vix.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-26 21:04:53
@Email        : cuixuanstephen@gmail.com
@Description  : 对 VIX 的交互式金融分析
"""

# from alpha_vantage.timeseries import TimeSeries
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# with open("../token/alphavantage.txt", "r") as f:
#     # 毫无用处的数据提供商，废物
#     ALPHA_VANTAGE_API_KEY = "P38R88UAK4883K9H"
# ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format="pandas")
# df_spx_data, meta_data = ts.get_daily(symbol="^GSPC", outputsize="full")
try:
    df_spx_data = yf.download("^GSPC", start="2000-01-01", end="2018-12-31")
except:
    df_spx_data = pd.read_csv("./data/SPX.csv", parse_dates=["Date"], index_col="Date")

try:
    df_vix_data = yf.download("^VIX", start="2000-01-01", end="2018-12-31")
except:
    df_vix_data = pd.read_csv("./data/VIX.csv", parse_dates=["Date"], index_col="Date")

df = pd.DataFrame({"SPX": df_spx_data["Adj Close"], "VIX": df_vix_data["Adj Close"]})

plt.figure(figsize=(12, 8))
ax_spx = df["SPX"].plot()
ax_vix = df["VIX"].plot(secondary_y=True)
ax_spx.legend(loc=1)
ax_vix.legend(loc=2)
# plt.show()

df.diff().hist(figsize=(10, 5), color="blue", bins=100)
df.pct_change().hist(figsize=(10, 5), color="blue", bins=100)

log_returns = df.apply(np.log).diff().dropna()
log_returns.plot(subplots=True, figsize=(10, 8), color="blue", grid=True)
for ax in plt.gcf().axes:
    ax.legend(loc="upper left")

log_returns.plot(figsize=(10, 8), x="SPX", y="VIX", kind="scatter")
ols_fit = sm.OLS(log_returns["VIX"].values, log_returns["SPX"].values).fit()
plt.plot(log_returns["SPX"], ols_fit.fittedvalues, "r")

df_corr = df["SPX"].rolling(252).corr(other=df["VIX"])
df_corr.plot(figsize=(12, 8))
plt.ylabel("Rolling Annual Correlation")
