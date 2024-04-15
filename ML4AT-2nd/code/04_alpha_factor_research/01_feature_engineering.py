import warnings

warnings.filterwarnings("ignore")

from datetime import datetime
import pandas as pd
import pandas_datareader.data as web
from statsmodels.regression.rolling import RollingOLS

import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
idx = pd.IndexSlice
