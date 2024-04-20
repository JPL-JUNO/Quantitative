"""
@File         : financial_pattern_recognition.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-20 16:58:03
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import matplotlib.pyplot as plt
import pandas as pd


class FinancialPatternRecognition:
    def __init__(self) -> None:
        pass

    def show_signal(self, data: pd.DataFrame, underlying, markersize=4, dpi: int = 500):
        fig, ax = plt.subplots(figsize=(18, 6))
        ax.plot(data["Close"], linewidth=2, label="Close")
        long = data["signal"] == 1
        short = data["signal"] == -1

        ax.plot(
            data[long]["Close"],
            marker="^",
            linestyle="None",
            color="red",
            markersize=markersize,
            label="Long",
        )

        ax.plot(
            data[short]["Close"],
            marker="v",
            linestyle="None",
            color="purple",
            markersize=markersize,
            label="Short",
        )

        plt.legend()
        plt.title(f"{underlying} {self.pattern}")
        plt.tight_layout()
        plt.savefig(f"./figures/{underlying}_{self.pattern}.png", dpi=dpi)
