"""
@File         : plot.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-23 21:48:59
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import matplotlib.pyplot as plt
import pandas as pd


def show_signal(data: pd.DataFrame, markersize=4, dpi: int = 500, **kwargs):
    fig, ax = plt.subplots(figsize=(18, 6))
    ax.plot(data["close"], linewidth=2, label="close")
    long = data["signal"] == 1
    short = data["signal"] == -1

    ax.plot(
        data[long]["close"],
        marker="^",
        linestyle="None",
        color="red",
        markersize=markersize,
        label="Long",
    )

    ax.plot(
        data[short]["close"],
        marker="v",
        linestyle="None",
        color="purple",
        markersize=markersize,
        label="Short",
    )

    plt.legend()
    underlying = kwargs.get("underlying", "underlying")
    pattern = kwargs.get("pattern", "strategy")
    plt.title(f"{underlying} {pattern}")
    plt.tight_layout()
    save = kwargs.get("save", None)
    if save:
        plt.savefig(f"./figures/{underlying}_{pattern}.png", dpi=dpi)
