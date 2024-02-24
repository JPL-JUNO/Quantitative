"""
@File         : ch08.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-24 20:54:06
@Email        : cuixuanstephen@gmail.com
@Description  : 金融基本概念
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="金融基本概念",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)
st.title("金融基本概念")
st.subheader("Stephen CUI")
st.subheader("2024-02-24")
tabs = st.tabs(
    [
        "收益率",
        "对数收益率",
        "年化收益",
        "波动率",
        "夏普比率",
        "索提诺比率",
        "阿尔法和贝塔",
        "最大回撤",
    ]
)
with tabs[0]:
    st.markdown(
        "假设 $P_t$ 表示在时刻 $t$ 时一种资产的价格，在没有利息的情况下，从时刻 $t-1$ 到时刻 $t$ 这一持有阶段的收益率为："
    )
    st.latex(
        r"""
    \begin{equation}
    R_r=\frac{P_t-P_{t-1}}{P_{t-1}}
    \end{equation}
    """
    )
    st.markdown(
        """
    其中，分子 $P_t-P_{t-1}$ 表示资产在持有期内的收入或利润，如果该值为负，则表示亏损。分母 $P_{t-1}$ 表示持有资产初期的原始投资。
    """
    )

with tabs[1]:
    st.markdown(
        """
    对数收益率（Log returns），用 $r_t$ 表示。$r_t$ 的定义如下：
    """
    )
    st.latex(
        r"""
        \begin{equation}
        r_t=\ln(1+R_t)=\ln\frac{P_t}{P_{t-1}}
        \end{equation}
        """
    )
with tabs[2]:
    st.markdown(
        """
    年化收益（Annualized Returns）表示资产平均每年能有多少收益。我们在对比资产的收益的时候，需要有一个统一的标准。计算方式是：
    """
    )
    st.latex(
        r"""
        r_t * \frac{250}{T_{t}-T_{t-1}}
    """
    )
    st.markdown(
        """
    **年化收益的一个直观的理解是，假设按照某种盈利能力，换算成一年的收益大概能有多少**。这个概念常常会存在误导性。
    """
    )
with tabs[3]:
    st.markdown(
        """
        波动率（Volatility）是用来衡量收益率的不确定性的。波动率可以定义为收益率的标准差，即
    """
    )
    st.latex(
        r"""
        \sigma=std(r)
    """
    )
    st.markdown(
        """
    假设不同时间段的收益率没有相关性（称为没有自相关性），那么可以证明的是，收益率的方差 $Var(r)$ 具有时间累加性。时间累加性的意思是，不同时间段 $t_1, t_2,\dots,t_n$ 的方差，加总即可得到 $t_1, t_2,\dots,t_n$ 这段时间的方差。随着时间的增加，方差将会成正比增加，波动率（标准差）将会按时间开根号的比例增加。举个例子，假设股票收益率的日波动率为 $\sigma$ ，那么股票每年的波动率就为 $\sqrt{250}\sigma$。
    
    这种不同周期间的波动率换算，在投资计算中非常常见。最常用的波动率是年化波动率，我们经常需要将日波动率、月波动率换算成年化波动率。
    """
    )
with tabs[4]:
    st.markdown(
        """
        夏普比率描述的正是这每承受一单位的风险，会产生多少超额的报酬。用数学公式描述就是：
    """
    )
    st.latex(
        r"""
        \begin{equation}
        \text{sharpe ratio}=\frac{E(R_p)-R_f}{\sigma_p}
        \end{equation}
    """
    )
    st.markdown(
        """
        式中，$E(R_p)$ 表示资产（组合）的预期收益率，$R_f$ 表示无风险利率，一般用国债利率替换，$\sigma_p$ 表示资产（组合）的波动率。收益率和波动率只能使用历史数据估算。这三个指没有特殊说明表示年化后的值。
        
        对比策略优劣的时候，周期要一致，比如，对比每日调仓的策略和每月调仓的策略，一定要换算到同一个周期上，才有可比性。
    """
    )
with tabs[5]:
    st.markdown(
        """
        索提诺比率与夏普比率相似，不一样的是，索提诺比率是使用下行风险来衡量波动率的。在夏普比率中，资产大涨与资产大跌都可视为波动风险。
    """
    )

with tabs[6]:
    st.markdown(
        """
        阿尔法策略，其实是来源于资本资产定价模型（CAPM）。这个模型将股票的收益分为了两个部分，一部分是由大盘涨跌带来的，另一部分则是由股票自身的特性带来的。大盘的那部分影响就是贝塔（Beta）值，剔除大盘的影响，剩下的股票自身就是 Alpha 值。在谈论 Alpha 策略的时候，其实就是在谈论股票与大盘无关的那部分超额收益。如果 Alpha 策略做得好，对冲掉大盘风险后，可以取得相当稳定的收益。
    """
    )
# 生成一些工作日（假设为交易日）以及收益率
df = pd.DataFrame(
    {
        "trade_date": pd.date_range("2023-01-01", "2024-02-24", freq="B"),
        "rtn": np.random.standard_normal(size=300) / 100,
    }
)
# 计算累积收益率
df["cumsum"] = 1 + df["rtn"].cumsum()
df["cummax"] = df["cumsum"].cummax()
max_dropdown = np.max(1 - df["cumsum"] / df["cummax"]) * 100
df["dropdown"] = 1 - df["cumsum"] / df["cummax"]
fig, ax = plt.subplots()
df[["cumsum", "cummax"]].plot(ax=ax)
idx_max_dropdown = df["dropdown"].idxmax()
idx_max_dropdown_cumsum = df.iloc[:idx_max_dropdown]["cumsum"].idxmax()

ax.annotate(
    text="max",
    xy=(idx_max_dropdown_cumsum, df.iloc[idx_max_dropdown_cumsum]["cumsum"] * 1.01),
)
ax.annotate(
    text="min", xy=(idx_max_dropdown, df.iloc[idx_max_dropdown]["cumsum"] * 0.98)
)
ax.plot([idx_max_dropdown_cumsum], [df.iloc[idx_max_dropdown_cumsum]["cumsum"]], "rv")
ax.plot([idx_max_dropdown], [df.iloc[idx_max_dropdown]["cumsum"]], "g^")
ax.set_ylim(df["cumsum"].min() * 0.95, 1.05 * df["cumsum"].max())
ax.set_title(f"Max Dropdown={max_dropdown:.4}%")
with tabs[7]:
    st.markdown(
        """
        最大回撤，顾名思义，是指投资一项资产，可能产生的最大亏损，即所谓的“买在最高点，抛在最低点”。
    """
    )
    st.latex(
        r"""
        \max\left(1-\frac{\text{当日累积收益}}{当前累积收益最大值}\right)
    """
    )
    st.pyplot(fig)
