"""
@Title: get_action_log_string and get_result_log_string
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-11-15 21:24:39
@Description: 
"""
import backtrader as bt


class MyBuySell(bt.observers.BuySell):
    """自定义买卖信号点

    Parameters
    ----------
    bt : bt.observers.BuySell
        _description_
    """
    plotlines = dict(
        buy=dict(marker="^", markersize=8.0, color='green', fillstyle='fill'),
        sell=dict(marker="v", markersize=8.0, color='red', fillstyle='fill'),
    )


def get_action_log_string(dir: str, action: str, price: float, size: int, asset: str = None,
                          cost: float = None, commission: float = None,
                          cash: float = None, open: float = None, close: float = None) -> str:
    """Helper function for logging. Creates a string indicating a 
    created/executed buy/sell order.

    Parameters
    ----------
    dir : str
        买卖方向，b or s
    action : str
        行为，e 执行，c 创建
    price : float
        价格
    size : int
        数量
    asset : str, optional
        资产名称, by default None
    cost : float, optional
        成本, by default None
    commission : float, optional
        佣金, by default None
    cash : float, optional
        现金, by default None
    open : float, optional
        开盘价格, by default None
    close : float, optional
        收盘价格, by default None

    Returns
    -------
    str
        日志的记录
    """
    dir_dict = {
        'b': 'BUY',
        's': 'SELL'
    }
    action_dict = {
        'e': 'EXECUTED',
        'c': 'CREATED'
    }
    output_string = (
        f'{dir_dict[dir]} {action_dict[action]} - '
        f'Price: {price:.2f}, Size: {size:.2f}'
    )
    if asset is not None:
        output_string = output_string + f', Asset: {asset}'

    if action == 'e':
        if cost is not None:
            output_string = output_string + f', Cost: {cost:.2f}'
        if commission is not None:
            output_string = output_string + f', Commission: {commission:.2f}'
    elif action == 'c':
        if cash is not None:
            output_string = output_string + f', Cash: {cash:.2f}'
        if open is not None:
            output_string = output_string + f', Open: {open:.2f}'
        if close is not None:
            output_string = output_string + f', Close: {close:.2f}'

    return output_string


def get_result_log_string(gross: float, net: float) -> str:
    """Helper function for logging. Creates a string indicating the summary of
    an operation.

    Parameters
    ----------
    gross : float
        总结果
    net : float
        净结果

    Returns
    -------
    str
        The string used for logging
    """
    output_string = f'OPERATION RESULT - Gross: {gross:.2f}, Net: {net:.2f}'
    return output_string
