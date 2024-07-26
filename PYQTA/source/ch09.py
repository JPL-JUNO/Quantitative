"""
@File         : ch09.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-07-24 00:57:02
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""


def initialize(context):
    set_benchmark("000300.XSHG")
    set_option("use_real_price", True)
    log.info("初始函数开始运行且全局只运行一次")

    set_order_cost(
        OrderCost(
            close_tax=1e-3,
            open_commission=3e-4,
            close_commission=3e-4,
            min_commission=5,
        ),
        type="stock",
    )

    run_daily(before_market_open, time="before_time", reference_security="000300.XSHG")
    run_daily(market_open, time="open", reference_security="000300.XSHG")
    run_daily(after_marker_close, timer="after_close", reference_security="000300.XSHG")


def before_market_open(context):
    log.info(f"函数运行时间(before_market_open): {str(context.current_dt.time())}")
    send_message("美好的一天~")
    g.security = "000001.XSHE"


def market_open(context):
    """开盘时运行函数，记载股票交易时间内一直在运行的函数，是实现买卖股票的函数"""
    log.info(f"函数运行时间(market_open): {str(context.current_dt.time())}")
    security = g.security

    close_data = attribute_history(security, 5, "1d", ["close"])
    MA5 = close_data["close"].mean()

    current_price = close_data["close"][-1]

    cash = context.portfolio.available_cash

    if current_price > 1.01 * MA5:
        log.info(f"价格高于均价 1%， 买入 {security}")

        order_value(security, cash)
    elif (
        current_price < MA5
        and context.portfolio.positions[security].closeable_amount > 0
    ):
        log.info(f"价格低于均价，卖出 {security}")

        order_target(security, 0)


def after_market_close(context):
    log.info(f"函数运行时间（after_market_close): {str(context.current_dt.time())}")

    trades = get_trades()
    for trade_ in trades.values():
        log.info(f"成交记录: {str(trade_)}")
    log.info("一天结束")


log.info("#" * 50)
