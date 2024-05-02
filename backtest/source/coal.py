"""
@File         : coal.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-24 21:12:27
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
from talib import RSI
import sys
from os import path

sys.path.append(path.join(path.dirname(__file__), ".."))
from utils.plot import show_signal

df = pd.read_csv("./data/515220.csv")
show_signal(df)
