"""
@File         : mfpr.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-16 20:20:25
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import datetime
import pytz
import pandas as pd
import MetaTrader5 as mt5
import matplotlib.pyplot as plt
import numpy as np
from data.quotes import get_quotes

frame_H1 = mt5.TIMEFRAME_H1
frame_D1 = mt5.TIMEFRAME_D1
now = datetime.datetime.now()

assets = [
    "EURUSD",
    "USDCHF",
    "GBPUSD",
    "USDCAD",
    "BTCUSD",
    "ETHUSD",
    "XAUUSD",
    "SP500m",
    "UK100",
]


def mass_import(asset: int, time_frame: str) -> np.ndarray:
    if time_frame == "H1":
        data = get_quotes(frame_H1, 2013, 1, 1, asset=assets[asset])
    elif time_frame == "D1":
        data = get_quotes(frame_D1, 2013, 1, 1, asset=assets[asset])
    data = data.iloc[:, 1:5].values
    data = data.round(decimals=5)
    return data
