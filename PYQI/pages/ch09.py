"""
@File         : ch09.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-25 23:11:50
@Email        : cuixuanstephen@gmail.com
@Description  : 资产定价入门
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="金融基本概念",
)
st.title("金融基本概念")
st.subheader("Stephen CUI")
st.subheader("2024-02-24")
tabs = st.tabs(
    [
        "利率",
        "利率的计量",
        "零息利率",
        "债券定价",
        "夏普比率",
        "索提诺比率",
        "阿尔法和贝塔",
        "最大回撤",
    ]
)
with tabs[0]:
    st.markdown(
        """
    无风险利率的选取并没有一个完全客观的标准，在美国，有交易员用一年期的国债利率作为无风险利率，但也有交易员认为政府债券隐含的利率是偏低的，所以很多金融机构将 LIBOR 作为无风险利率。2007 年发生信用危机导致 LIBOR 利率激增，许多市场参与者开始使用隔夜指数互换利率（Overnight Indexed Swap，OIS）作为对无风险利率的近似取值。在国内， SHIBOR 和 10 年期国债利率都可以作为无风险利率。
    """
    )
with tabs[1]:
    st.markdown(
        """
    假设将 $A$ 资金投资 $n$ 年。如果利率是按年复利的，那么投资的终值为：
    """
    )
    st.latex(
        r"""
    A(1+R)^n
    """
    )
    st.markdown(
        """
    如果利率是对应于一年复利 $m$ 次，那么投资终值为：
    """
    )
    st.latex(
        r"""
    \begin{equation}
    A\left(1+\frac{R}{m}\right)^{mn}
    \end{equation}
    """
    )
    fig, ax = plt.subplots(1, 1)
    data = pd.DataFrame({"frequency": np.arange(1, 15)})
    data["final_value"] = 100 * (1 + 0.1 / data["frequency"]) ** data["frequency"]
    data.plot(x="frequency", y="final_value", style="o-", ax=ax)
    ax.hlines(100 * np.exp(0.1), xmin=0, xmax=15, linestyles="--")
    st.pyplot(fig)
    st.caption("随着复利频率的增加，投资终值趋近于一个极限")
    st.markdown(
        """
    可以从数学上进行证明，当复利频率趋于无穷大的时候，投资的终值为：
    """
    )
    st.latex(
        r"""
    \begin{equation}
    Ae^{Rn}
    \end{equation}
    """
    )
    st.markdown(
        """
        在实际情况下，由于每天计算复利的频率非常高（每年复利 365次），非常接近于连续复利，因此可以认为普通复利的计算方法与连续复利的计算方法是等价的。对一笔资金，以利率 $R$ 连续复利 $n$ 年，相当于乘以 $e^{Rn}$。
        
        假设 $R^c$ 是连续复利利率，$R^m$ 是与之等价的每年 $m$ 次复利利率。有：
    """
    )
    st.latex(
        r"""
    \begin{equation}
    e^{R_cn}=\left(1+\frac{R_m}{m}\right)^{mn}
    \end{equation}
    """
    )
    st.markdown(
        """
        用这个公式可以对 $m$ 次复利利率和连续复利利率进行相互转换，有：
    """
    )
    st.latex(
        r"""
    \begin{equation}
    \begin{aligned}
    R_c&=m\ln\left(1+\frac{R_m}{m}\right)\\
    R_m&=m\left(e^{\frac{R_c}{m}}-1\right)\\
    \end{aligned}
    \end{equation}
    """
    )

with tabs[2]:
    st.markdown(
        """
        $N$ 年的零息利率（zero rate）是指今天投入的资金在 $N$ 年后所得的收益率。所有的利息以及本金在 $N$ 年末支付给投资者，在 $N$ 年满期之前，投资不支付任何利息收益。零息利率也称作即期利率（spot rate）。
    """
    )

with tabs[3]:
    st.markdown(
        """
    ### 债券收益率
    债券收益率又称为到期收益率（Yield To Maturity，YTM）。债券收益率等于对所有现金流贴现并使债券的价格与市场价格相等的贴现率。
    
    ```python
    import numpy as np
    from functools import partial
    from scipy.optimize import fsolve

    cash_flow = np.array([3, 3, 3, 103])
    t = np.arange(0.5, 2.5, 0.5)
    price = 98.39


    def func(y, cash_flow, t, price):
        return np.sum(cash_flow * np.e ** (-y * t)) - price


    y = fsolve(func, 0.1, args=(cash_flow, t, price))
    # func = partial(func, cash_flow=cash_flow, t=t, price=price)
    # y = fsolve(func, 0.1)
    print(y)
    ```
    ### 平价收益率
    """
    )
