"""
@Title        : 
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2023-12-10 19:20:40
@Description  : 
"""
import pandas as pd
import numpy as np
from pandas import DataFrame
from pandas.core.groupby.generic import DataFrameGroupBy

from binance.spot import Spot as Client


def get_bars(df: DataFrameGroupBy, add_time=False) -> DataFrame:
    ohlc = df['price'].ohlc()
    # volume-weighted average price
    vwap = df.apply(lambda x: np.average(
        x['price'], weights=x['qty'])).to_frame('vwap')

    vol = df['qty'].sum().to_frame('vol')
    cnt = df['qty'].size().to_frame('cnt')

    if add_time:
        time = df['time'].last().to_frame('time')
        res = pd.concat([time, ohlc, vwap, vol, cnt], axis=1)
    else:
        res = pd.concat([ohlc, vwap, vol, cnt], axis=1)

    return res


if __name__ == '__main__':
    spot_client = Client(base_url='https://api3.binance.com')
    r = spot_client.trades('BTCEUR')

    df = pd.DataFrame(r).drop(columns=["isBuyerMaker", "isBestMatch"])
    df['time'] = pd.to_datetime(df['time'], unit='ms')

    for column in ['price', 'qty', 'quoteQty']:
        df[column] = pd.to_numeric(df[column])

    df_grouped_time = df.groupby(pd.Grouper(key='time', freq='1Min'))
    time_bars = get_bars(df_grouped_time)
