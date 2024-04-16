"""
@File         : quotes.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-16 20:28:50
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import datetime
import pytz
import pandas as pd
import MetaTrader5 as mt5
from pandas import DataFrame


def get_quotes(time_frame, year=2005, month=1, day=1, asset="EURUSD") -> DataFrame:
    if not mt5.initialize():
        print(f"initialize() failed, error code = {mt5.last_error()}")
        quit()
    timezone = pytz.timezone("Europe/Paris")

    time_from = datetime.datetime(year, month, day, tzinfo=timezone)
    time_to = datetime.datetime.now(timezone) + datetime.timedelta(days=1)
    rates = mt5.copy_rates_range(asset, time_frame, time_from, time_to)
    rates_frame = pd.DataFrame(rates)

    return rates_frame
