"""
@File         : logisticRegression.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-09 16:14:28
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
import matplotlib.pyplot as plt


class LogisticRegressionVectorBacktest(object):
    def __init__(self, symbol, start, end, amount, tc, model) -> None:
        self.symbol = symbol
        self.start = start
        self.end = end
        self.amount = amount
        self.tc = tc
        if model == "regression":
            self.model = LinearRegression()
        elif model == "logistic":
            self.model = LogisticRegression(
                C=1e6, solver="lbfgs", multi_class="ovr", max_iter=1000
            )
        else:
            raise ValueError("Model not known or not yet implemented.")
        self.get_data()

    def get_data(self):
        raw = pd.read_csv(
            "data/pyalgo_eikon_eod_data.csv", index_col=0, parse_dates=True
        ).dropna()
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start : self.end]
        raw.rename(columns={self.symbol: "price"}, inplace=True)
        raw["returns"] = raw["price"].apply(np.log).diff()
        self.data = raw.dropna()

    def select_data(self, start, end) -> pd.DataFrame:
        data = self.data[(self.data.index >= start) & (self.data.index <= end)].copy()
        return data

    def prepare_features(self, start, end):
        self.data_subset = self.select_data(start, end)
        self.feature_columns = []
        for lag in range(1, self.lags + 1):
            col = f"lag_{lag}"
            self.data_subset[col] = self.data_subset["returns"].shift(lag)
            self.feature_columns.append(col)
        self.data_subset.dropna(inplace=True)

    def fit_model(self, start, end):
        self.prepare_features(start, end)
        self.model.fit(
            self.data_subset[self.feature_columns], np.sign(self.data_subset["returns"])
        )

    def run_strategy(self, train_start, train_end, test_start, test_end, lags=3):
        self.lags = lags
        self.fit_model(train_start, train_end)

        self.prepare_features(test_start, test_end)
        prediction = self.model.predict(self.data_subset[self.feature_columns])
        self.data_subset["prediction"] = prediction
        self.data_subset["strategy"] = (
            self.data_subset["prediction"] * self.data_subset["returns"]
        )

        trades = self.data_subset["prediction"].diff().fillna(0) != 0
        self.data_subset.loc[trades, "strategy"] -= self.tc
        self.data_subset["cum_returns"] = self.amount * self.data_subset[
            "returns"
        ].cumsum().apply(np.exp)
        self.data_subset["cum_strategy"] = self.amount * self.data_subset[
            "strategy"
        ].cumsum().apply(np.exp)

        self.results = self.data_subset

        aperf = self.results["cum_strategy"].iloc[-1]

        operf = aperf - self.results["cum_returns"].iloc[-1]
        return round(aperf, 2), round(operf, 2)

    def plot_results(self):
        if not hasattr(self, "results"):
            raise AttributeError("No results to plot yet. Run a strategy.")
        title = f"symbol={self.symbol}_TC={self.tc:.4f}"
        self.results[["cum_returns", "cum_strategy"]].plot(title=title, figsize=(10, 6))
        plt.axhline(self.amount, color="red", linestyle=":")


if __name__ == "__main__":
    scibt = LogisticRegressionVectorBacktest(
        ".SPX", "2010-1-1", "2019-12-31", 10000, 0.0, "regression"
    )
    print(scibt.run_strategy("2010-1-1", "2019-12-31", "2010-1-1", "2019-12-31"))
    print(scibt.run_strategy("2010-1-1", "2016-12-31", "2017-1-1", "2019-12-31"))
    scibt = LogisticRegressionVectorBacktest(
        ".SPX", "2010-1-1", "2019-12-31", 10000, 0.0, "logistic"
    )
    print(scibt.run_strategy("2010-1-1", "2019-12-31", "2010-1-1", "2019-12-31"))
    print(scibt.run_strategy("2010-1-1", "2016-12-31", "2017-1-1", "2019-12-31"))
    scibt = LogisticRegressionVectorBacktest(
        ".SPX", "2010-1-1", "2019-12-31", 10000, 0.00025, "logistic"
    )
    print(
        scibt.run_strategy("2010-1-1", "2019-12-31", "2010-1-1", "2019-12-31", lags=3)
    )
    print(
        scibt.run_strategy("2010-1-1", "2013-12-31", "2014-1-1", "2019-12-31", lags=5)
    )
