"""
@File         : ema.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-13 14:19:50
@Email        : cuixuanstephen@gmail.com
@Description  : 回测指数平均
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brute
import sys
from os import path
from pathlib import Path
import logging

plt.rcParams["savefig.dpi"] = 300
plt.rcParams["figure.dpi"] = 300
plt.rcParams["figure.figsize"] = (18, 10)
plt.style.use("ggplot")

sys.path.append(path.join(path.dirname(__file__), "../../"))
from source.trend import Trend
from talib import EMA
import logging


class TAEMA(Trend):
    def __init__(self, fast=13, slow=26) -> None:
        self.fast = fast
        self.slow = slow
        self.mkdir()

    def mkdir(self):
        self.results_path = Path("./figures/ema/") / f"{self.fast}_{self.slow}"
        self.hit_ratio_path = self.results_path / "hit_ratio"
        self.results_path.mkdir(parents=True, exist_ok=True)
        self.hit_ratio_path.mkdir(parents=True, exist_ok=True)
        logging_path = Path(f"./log/")
        logging_path.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(filename=logging_path / "ema.log", level=logging.INFO)
        self.logger = logging.getLogger(f"{self.fast}_{self.slow}")

    def load_data(self, underlying):
        self.current_underlying = underlying
        raw = pd.read_csv(
            f"./data/{underlying}.csv", parse_dates=["date"], thousands=","
        )
        fast = EMA(raw["close"], self.fast)
        slow = EMA(raw["close"], self.slow)

        raw["EMA_fast"] = fast
        raw["EMA_slow"] = slow

        self.data = raw.copy()

    def calculate_returns(self):
        self.data["return"] = self.data["close"].apply(np.log).diff()
        self.data.dropna(inplace=True)

    def signal_logic(self):
        indicator = self.data.copy()
        indicator["signal"] = np.where(
            indicator["EMA_fast"] > indicator["EMA_slow"], 1, 0
        )
        self.indicator = indicator.copy()

    def strategy_returns(self):
        self.indicator["strategy_returns"] = (
            self.indicator["return"].shift(-1) * self.indicator["signal"]
        )

        self.indicator = self.indicator.dropna().reset_index(drop=True)

    def compare_returns(self) -> tuple[float, float]:
        self.indicator["cum_bh"] = self.indicator["return"].cumsum().apply(np.exp)
        self.indicator["cum_strategy"] = (
            self.indicator["strategy_returns"].cumsum().apply(np.exp)
        )
        return (
            self.indicator["cum_strategy"].iloc[-1],
            self.indicator["cum_bh"].iloc[-1],
        )

    def stats_hit_ratios(self) -> float:
        oci = self.open_close_price()
        oci["hit_ratio"] = (oci["returns"] > 0).cumsum().div(oci.index + 1)
        fig, axes = plt.subplots(2, 1, sharex=True)
        axes[0].stem(oci["returns"])
        axes[1].plot(oci["hit_ratio"])
        plt.tight_layout()
        plt.savefig(self.hit_ratio_path / f"{self.current_underlying}.png")

        return oci["hit_ratio"].iloc[-1]

    def open_close_index(self):
        data = self.indicator.copy()
        data["series_num"] = (data["signal"] != data["signal"].shift()).cumsum()

        open2close = data.groupby("series_num").apply(
            lambda grp: pd.Series(
                {
                    "open_index": grp.index[0],
                    "close_index": grp.index[-1] + 1,
                    "hold": grp["signal"].mean(),
                    "hold_days": len(grp) + 1,
                },
                dtype=int,
            ),
            include_groups=False,
        )
        mask = open2close["hold"] == 1
        open2close.drop(labels=["hold"], inplace=True, axis=1)
        open2close = open2close.loc[mask].reset_index(drop=True)
        return open2close

    def open_close_price(self) -> pd.DataFrame:
        oc_info = {}
        o_c_index = self.open_close_index()
        for idx, meta in o_c_index.iterrows():
            data = self.indicator.iloc[meta["open_index"] : meta["close_index"] + 1]
            oc_info[idx] = {
                "open_price": data["close"].iloc[0],
                "close_price": data["close"].iloc[-1],
                "open_date": data["date"].iloc[0],
                "close_date": data["date"].iloc[-1],
                "hold_days": meta["hold_days"],
            }
        oci = pd.DataFrame(oc_info.values())
        oci["returns"] = np.log(oci["close_price"]) - np.log(oci["open_price"])
        return oci


if __name__ == "__main__":
    ema = TAEMA()
    ema.load_data(underlying="510880")
    # ema.backtest()
    # ema.plot_results()
    # ema.open_close_index()
