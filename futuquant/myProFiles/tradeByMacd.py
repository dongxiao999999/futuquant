# -*- coding: utf-8 -*-
"""
验证接口：下单然后立即撤单, 为避免成交损失，买单价格港股放在十档，美股为一档下降10%, 买单数量为1手（美股为1股）
"""
from time import sleep
import sys
import os

from futuquant.myProFiles import stockData

sys.path.append(os.path.split(os.path.abspath(os.path.pardir))[0])

from futuquant.open_context import *

'''
  验证接口：下单然后立即撤单, 为避免成交损失，买单价格港股放在十档，美股为一档下降10%, 买单数量为1手（美股为1股）
  使用请先配置正确参数:
  api_svr_ip: (string)ip
  api_svr_port: (string)ip
  unlock_password: (string)交易解锁密码, 必需修改！！！
  test_code: (string)股票
  trade_env: (int)0 真实交易 1仿真交易  ( 美股暂不支持仿真）
'''


def make_order_and_cancel(api_svr_ip, api_svr_port, unlock_password, test_code, trade_env):
    """
    使用请先配置正确参数:
    :param api_svr_ip: (string) ip
    :param api_svr_port: (string) ip
    :param unlock_password: (string) 交易解锁密码, 必需修改!
    :param test_code: (string) 股票
    :param trade_env: (int) 0: 真实交易 1: 仿真交易 (美股暂不支持仿真)
    """
    if unlock_password == "":
        raise Exception("请先配置交易解锁密码!")

    quote_ctx = OpenQuoteContext(host=api_svr_ip, port=api_svr_port)  # 创建行情api
    quote_ctx.subscribe(test_code, "ORDER_BOOK", push=False)  # 定阅摆盘

    # 创建交易api
    is_hk_trade = 'HK.' in test_code
    if is_hk_trade:
        trade_ctx = OpenHKTradeContext(host=api_svr_ip, port=api_svr_port)
    else:
        if trade_env != 0:
            raise Exception("美股交易接口不支持仿真环境")
        trade_ctx = OpenUSTradeContext(host=api_svr_ip, port=api_svr_port)

    # 每手股数
    lot_size = 0
    is_unlock_trade = False
    is_fire_trade = False
    order_id = 0
    while True:
        sleep(2)
        # 解锁交易
        if not is_unlock_trade:
            ret_code, ret_data = trade_ctx.unlock_trade(unlock_password)
            is_unlock_trade = (ret_code == 0)
            if not trade_env and not is_unlock_trade:
                print("请求交易解锁失败：{}".format(ret_data))
                continue

        if lot_size == 0:
            ret, data = quote_ctx.get_market_snapshot([test_code])
            lot_size = data.iloc[0]['lot_size'] if ret == 0 else 0
            if ret != 0:
                print("取不到每手信息，重试中!")
                continue
            elif lot_size <= 0:
                raise BaseException("该股票每手信息错误，可能不支持交易 code ={}".format(test_code))

        ret, data = quote_ctx.get_order_book(test_code)  # 得到第十档数据
        if ret != 0:
            continue

        # 计算交易价格
        bid_order_arr = data['Bid']
        ask_order_arr = data['Ask']
        if is_hk_trade:
            if len(bid_order_arr) != 10:
                continue
            # 港股下单: 价格定为买一档与卖一档的平均值
            price1, _, _ = bid_order_arr[0]
            price2, _, _ = ask_order_arr[0]
            # price = round((price1 + price2) / 2, 2)
            price = round((price2 * 1.0001), 2)
        else:
            if len(bid_order_arr) == 0:
                continue
            # 美股下单： 价格定为一档降10%
            price, _, _ = bid_order_arr[0]
            price = round(price * 0.9, 2)

        qty = lot_size

        # 价格和数量判断
        if qty == 0 or price == 0.0:
            continue

        # 交易类型
        order_side = 0  # 买
        if is_hk_trade:
            order_type = 0  # 港股增强限价单(普通交易)
        else:
            order_type = 2  # 美股限价单

        # 下单
        df = stockData.getCurKlines(quote_ctx, "HK.00700", "K_5M", 100)
        df = stockData.getMACD(df)
        curData = df.iloc[-1]  # 当前时间
        lastData = df.iloc[-2]  # 上一时间
        if curData['open'] == 0 or curData['close'] == 0:
            continue
        if order_id == 0:  # 未下单
            if curData['dif'] > 0 and curData['dea'] > 0:  # 0轴上方，多头
                if curData['macd'] > 0 and lastData['macd'] < 0:  # 0轴上方macd金叉,购买股票
                    ret_code, ret_data = trade_ctx.place_order(price=price2, qty=qty, strcode=test_code,
                                                               orderside=order_side, ordertype=order_type,
                                                               envtype=trade_env)
                    print('下单ret={} data={}'.format(ret_code, ret_data))
                    if ret_code == 0:
                        row = ret_data.iloc[0]
                        order_id = row['orderid']

        # 卖单
        if order_id != 0:
            order_side = 1
            if curData['dif'] < 0 and curData['dea'] < 0:  # 0轴下方，空头
                if (curData['macd'] < 0 and lastData['macd'] > 0) or curData['macdRatio'] > 1:  # 0轴上方macd死叉或者在0轴之前形成死叉，0轴之后放大,卖出股票
                    ret_code, ret_data = trade_ctx.place_order(price=price1, qty=qty, strcode=test_code,
                                                               orderside=order_side, ordertype=order_type,
                                                               envtype=trade_env)
                    print('卖单ret={} data={}'.format(ret_code, ret_data))
                    if ret_code == 0:
                        order_id = 0
            elif curData['dif'] > 0 and curData['dea'] > 0:  # 0轴上方
                if curData['macd'] < 0 and curData['macdRatio'] > 1:  # 0轴上方macd死叉或者在0轴之前形成死叉，0轴之后放大,卖出股票
                    ret_code, ret_data = trade_ctx.place_order(price=price1, qty=qty, strcode=test_code,
                                                               orderside=order_side, ordertype=order_type,
                                                               envtype=trade_env)
                    print('卖单ret={} data={}'.format(ret_code, ret_data))
                    if ret_code == 0:
                        order_id = 0
    # destroy object
    quote_ctx.close()
    trade_ctx.close()

def getPrice(quote_ctx, test_code, is_hk_trade):
    ret, data = quote_ctx.get_order_book(test_code)  # 得到第十档数据
    # 计算交易价格
    bid_order_arr = data['Bid']
    ask_order_arr = data['Ask']
    if is_hk_trade:
        # 港股下单: 价格定为买一档与卖一档的平均值
        price1, _, _ = bid_order_arr[0]
        price2, _, _ = ask_order_arr[0]
        price = round((price1 + price2) / 2, 2)
    else:
        # 美股下单： 价格定为一档降10%
        price, _, _ = bid_order_arr[0]
        price = round(price * 0.9, 2)
    return price


if __name__ == "__main__":
    API_SVR_IP = '127.0.0.1'
    API_SVR_PORT = 11111
    UNLOCK_PASSWORD = "Dx1111"
    TEST_CODE = 'HK.00700'  # 'US.BABA' 'HK.00700'
    TRADE_ENV = 1

    make_order_and_cancel(API_SVR_IP, API_SVR_PORT, UNLOCK_PASSWORD, TEST_CODE, TRADE_ENV)

