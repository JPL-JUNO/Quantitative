import jqdatasdk
from jqlib.technical_analysis import *


def initialize(context):
    g.security = "000001.XSHE"

    set_benchmark("000300.XSHE")
    set_option("use_real_price", True)


def handle_data(context, data):
    security = g.security

    macd_diff, macd_dea, macd_macd = MACD(
        security, check_date=context.current_dt, SHORT=12, LONG=26, MID=9
    )

    cash = context.portfolio.cash

    if macd_diff > 0 and macd_dea > 0 and macd_diff > macd_dea:
        order_value(security, cash)

        log.info(f"买入股票 {security}")
    elif (
        macd_diff < 0
        and macd_dea < 0
        and macd_diff < macd_dea
        and context.portfolio.positions[security].closeable_amount > 0
    ):
        order_target(security, 0)
        log.info(f"卖出股票 {security}")
