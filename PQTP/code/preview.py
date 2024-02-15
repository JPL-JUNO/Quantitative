"""
@File         : preview.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-01-30 22:02:11
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""
import pandas_datareader as web
import numpy as np
import pandas as pd


start_date = "2020-01-01"
end_date = "2020-03-18"

# data = web.data.DataReader("601318.ss", "stooq", start_date, end_date)
data = pd.read_csv("../data/601318_cn_d.csv", parse_dates=True, index_col=["Date"])
data = data.loc[start_date:end_date]
data["diff"] = data["Close"].diff()
data["signal"] = np.where(data["diff"] > 0, 1, 0)
