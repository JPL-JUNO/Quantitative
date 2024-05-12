"""
@File         : macd.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-12 00:11:00
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
import matplotlib.pyplot as plt
from talib import MACD
import numpy as np

plt.style.use("ggplot")

underlying = "600900"
data = pd.read_csv(f"./data/{underlying}.csv")
data["return"] = data["close"].apply(np.log).diff()
data["MACD_hist"] = MACD(data["close"], fastperiod=12, slowperiod=26, signalperiod=9)[2]
data["delta_macd"] = data["MACD_hist"].diff()
data.dropna(inplace=True)

data["signal"] = np.where(data["delta_macd"] > 0, 1, 0)

data["strategy"] = data["return"].shift(periods=-1) * data["signal"]
data["cum_strategy"] = data["strategy"].cumsum().apply(np.exp)
data["cum_bh"] = data["return"].cumsum().apply(np.exp)
data[["cum_bh", "cum_strategy"]].plot()
print(data["cum_strategy"].iloc[-2])
plt.show()
