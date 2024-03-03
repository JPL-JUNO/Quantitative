"""
@File         : interactive_financial_analytics_with_the_vix.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-26 19:28:28
@Email        : cuixuanstephen@gmail.com
@Description  : 对 VIX 的交互式金融分析
"""

import streamlit as st

st.title("对 VIX 的交互式金融分析")
st.subheader("Stephen CUI")
st.subheader("2024-02-26")
st.markdown(
    """
    对于利用 S&P 500 指数的基准策略，其与 VIX 负相关的性质为避免基准成本再平衡提供了一种可行的方法，波动率的统计性质允许交易者执行均值回归策略、分散交易和波动率价差交易等操作。
    """
)

tabs = st.tabs(
    ["波动率指数衍生品", "S&P 500 指数和 VIX 指数的金融分析", "计算 VIX 指数", "总结"]
)

with tabs[0]:
    st.markdown(
        """
    ### EURO STOXX 50 指数
    STOXX 有限公司设计的 EURO STOXX 50指数是全球最重要的股票指数之一，于 1998 年 2 月 26 日推出，由来自 12 个欧元区国家——奥地利、比利时、芬兰、法国、德国、希腊、爱尔兰、意大利、卢森堡、荷兰、葡萄牙和西班牙的 50 个蓝筹股股票组成。它的期货和期权合约可在欧洲期货交易所买卖。该指数基于实时价格，通常每 15 秒重新计算一次。
    ### VSTOXX
    VSTOXX 或 EURO STOXX 50 波动率是由欧洲期货交易所推出的波动率衍生产品。VSTOXX 市场指数基于一篮子 OESX 市场价格的平值或虚值报价测算，衡量未来 30 天内 EURO STOXX 50 指数的隐含市场波动率。
    ### S&P 500 指数
    S&P 500 指数（SPX）的历史可以追溯到 1923 年，当时它被称为综合指数（Composite Index）。最初，它只包含一小部分股票。1957 年，它的股票数量增加到了 500 只，然后成了现在的 SPX。
    ### SPX期权
    CBOE 提供多种期权合约供交易，包括股票指数（如 SPX）上的期权。
    ### VIX 指数
    与 STOXX 一样，CBOE 的 VIX 衡量 S&P 500 股票指数期权价格隐含的短期波动率。1993 年，CBOE VIX 开始以 S&P 100 指数为基础，2003 年更新以 SPX 为基础，2014 年再次更新包括 SPXW 期权。它每 15 秒重新计算一次，由 CBOE 分发，是测算未来 30 天股市波动的重要指标。
    """
    )
