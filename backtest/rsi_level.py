"""
@File         : rsi_level.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-27 15:17:37
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import pandas as pd
from talib import RSI, EMA, BBANDS, MACD
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

plt.rcParams["figure.figsize"] = (18, 10)
plt.rcParams["figure.dpi"] = 300


def impulse_system(row) -> int:
    ema_sign = np.sign(row["EMA_slope"])
    macd_sign = np.sign(row["MACD_slope"])
    if ema_sign + macd_sign == 2:
        return 1
    elif ema_sign + macd_sign == -2:
        return -1
    else:
        return 0


def divergences(row) -> int:
    mask1 = row["close"] == row["close_reach_low"]
    mask2 = row["RSI"] > row["rsi_reach_low"]
    if mask1 and mask2:
        return 1
    else:
        return 0


def filter_semi_signal(raw: pd.DataFrame, index: pd.Index) -> pd.Index:
    filter_mask = np.zeros_like(index)
    for idx, value in enumerate(index):
        if raw.at[value, "impulse"] == -1 and raw.at[value + 1, "impulse"] >= 0:
            filter_mask[idx] = 1
    return index[filter_mask == 1]


def generate_data():
    raw = pd.read_csv("./data/002555.csv", parse_dates=["date"])

    rsi = RSI(raw["close"], timeperiod=14)

    ema = EMA(raw["close"], timeperiod=10)

    macd, macd_signal, macd_hist = MACD(
        raw["close"], fastperiod=12, slowperiod=26, signalperiod=9
    )

    upper_band, mid_band, lower_band = BBANDS(raw["close"], timeperiod=14)

    raw = raw.assign(
        RSI=rsi,
        EMA=ema,
        MACD_hist=macd_hist,
        BBANDS_upper=upper_band,
        BBANDS_mid=mid_band,
        BBANDS_lower=lower_band,
    )

    raw["EMA_slope"] = raw["EMA"].diff()
    raw["MACD_slope"] = raw["MACD_hist"].diff()

    # 低点
    raw["close_reach_low"] = raw["close"].rolling(window=60).min()
    raw["rsi_reach_low"] = raw["RSI"].rolling(window=60).min()

    raw.dropna(inplace=True)
    raw.reset_index(drop=True, inplace=True)

    raw["impulse"] = raw.apply(impulse_system, axis=1)

    raw["divergences"] = raw.apply(divergences, axis=1)

    semi_auto_signal_index = raw[raw["divergences"] == 1].index

    st.session_state["semi_auto_signal_index"] = filter_semi_signal(
        raw, semi_auto_signal_index
    )

    return raw


if "raw" not in st.session_state:
    raw = generate_data()

    st.session_state["raw"] = raw

if "idx" not in st.session_state:
    st.session_state["idx"] = 0

if "balance" not in st.session_state:
    st.session_state["balance"] = 40000

impulse_map = {1: "red", 0: "blue", -1: "green"}


def reshow():
    index = st.session_state["semi_auto_signal_index"][st.session_state["idx"]]
    data = st.session_state["raw"].iloc[
        max(0, index - 179) : index + st.session_state["pattern_days"]
    ]
    if not data.empty:
        fig, ax = plt.subplots(2, 1, sharex=True)
        ax[0].scatter(
            data.index + 1,
            data["close"],
            c=data["impulse"].map(impulse_map).to_list(),
        )
        ax[0].plot(data.index + 1, data["close"])
        data[["BBANDS_upper", "BBANDS_mid", "BBANDS_lower"]].plot(
            ax=ax[0], linestyle="--", color="orange"
        )
        ax[1].plot(data.index + 1, data["RSI"])
        ax[1].axhline(0, color="black")
        ax[1].axhline(data.iloc[-1]["rsi_reach_low"], color="red", linestyle="-.")
        ax[0].axhline(data.iloc[-1]["close_reach_low"], color="red", linestyle="-.")
        plt.tight_layout()
        return fig, data.iloc[-1]


if st.button(label="Next Pattern"):
    st.session_state["idx"] += 1
    st.session_state["pattern_days"] = 1
    if st.session_state["idx"] < len(st.session_state["semi_auto_signal_index"]):
        fig, data = reshow()
        st.progress(
            st.session_state["idx"] / len(st.session_state["semi_auto_signal_index"])
        )

if st.button(label="Next Trade Day"):
    st.session_state["pattern_days"] += 1
    fig, data = reshow()
    st.session_state["end_index"] = st.session_state["pattern_days"]

try:
    st.pyplot(fig)
    st.json(data.to_json())
    # buy_or_sell = st.radio(label="Buy or Sell", options=["Pass", "Buy", "Sell"])
    # if buy_or_sell == "Buy":
    #     open_price = data["close"]
    #     st.session_state["open_price"] = data["close"]
    #     open_interest = (st.session_state["balance"] / open_price // 100) * 100
    #     st.session_state["open_interest"] = open_interest
    #     st.session_state["balance"] -= open_price * open_interest
    # elif buy_or_sell == "Sell":
    #     sell_price = data["close"]
    #     open_price = st.session_state["open_price"]

    #     pnl = (sell_price - open_price) * st.session_state["open_interest"]
    #     st.session_state["balance"] += sell_price * st.session_state["open_interest"]
    # st.write(st.session_state["balance"])
except NameError:
    pass
