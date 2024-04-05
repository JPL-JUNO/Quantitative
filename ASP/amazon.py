"""
@File         : amazon.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-04 15:21:08
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

sns.set_style("darkgrid")
from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    OneHotEncoder,
)
import warnings

warnings.filterwarnings("ignore")
import os
import plotly.graph_objects as go
import joblib
import itertools
from sklearn.metrics import (
    roc_auc_score,
    roc_curve,
    explained_variance_score,
    mean_squared_error,
    mean_absolute_error,
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    accuracy_score,
    recall_score,
    precision_score,
    classification_report,
    f1_score,
)
from sklearn.model_selection import (
    cross_val_score,
    train_test_split,
    RandomizedSearchCV,
    GridSearchCV,
    StratifiedKFold,
)
from statsmodels.tsa.seasonal import seasonal_decompose as season
from sklearn.linear_model import LogisticRegression, SGDClassifier
from pathlib import Path

curr_path = Path(os.getcwd())
df = pd.read_csv(curr_path / "Amazon.csv")
print(df.shape)
print("Data columns -->", list(df.columns))
print(df.info())
