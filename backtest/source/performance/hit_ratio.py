"""
@File         : hit_ratio.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-25 18:51:25
@Email        : cuixuanstephen@gmail.com
@Description  : 胜率计算
"""


def hit_ratio(data):
    # 如果最后一条数据显式 long，那么就还没有信号的表现，先移除
    long_df = data.loc[data["signal"] == 1].dropna()
    short_df = data.loc[data["signal"] == -1].dropna()
    if short_df.empty:
        print("没有 short 交易")
    profit = (long_df["hold_returns"] > 0).sum()
    try:
        return profit / len(long_df)
    except ZeroDivisionError:
        raise ValueError
