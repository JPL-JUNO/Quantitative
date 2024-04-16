"""
@File         : introducing_technical_analysis.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-16 20:14:01
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import matplotlib.pyplot as plt
import sys
from os import path

sys.path.append(path.join(path.dirname(__file__), "../"))
from mfpr import mass_import
from data.load_local_data import load_data

# Choosing the asset
pair = 0

# Time Frame
horizon = "D1"
# 狗屎
# my_data = mass_import(pair, horizon)

my_data = load_data("EURUSD_wrangled")
plt.plot(my_data, color="black", label="EURUSD")
plt.legend()
plt.grid()
