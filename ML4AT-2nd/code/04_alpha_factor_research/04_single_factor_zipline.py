"""
@File         : 04_single_factor_zipline.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-13 11:38:11
@Email        : cuixuanstephen@gmail.com
@Description  : Zipline Backtest with Single Factor
"""

import warnings

warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

from zipline.api import attach_pipeline
