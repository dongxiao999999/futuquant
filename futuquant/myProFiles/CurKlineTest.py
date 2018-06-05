from futuquant.open_context import *

from futuquant.open_context import CurKlineHandlerBase
from futuquant.myProFiles import stockData


class StockQuoteTest(StockQuoteHandlerBase):
    """
    获得报价推送数据
    """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(StockQuoteTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, content
        print("*异步回调接口 StockQuoteTest : %s" % content)
        return RET_OK, content


class CurKlineTest(CurKlineHandlerBase):
    """ kline push"""
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        if ret_code == RET_OK:
            print("*异步回调接口 CurKlineTest : %s\n" % content)
        return RET_OK, content


class OrderBookTest(OrderBookHandlerBase):
    """ 获得摆盘推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("* OrderBookTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("* OrderBookTest\n", content)
        return RET_OK, content


if __name__ == "__main__":
    stockCode = "HK.00700"
    sub_type = "K_5M"
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.set_handler(CurKlineTest())
    quote_ctx.set_handler(OrderBookTest())
    quote_ctx.start()
    ret_status, ret_data = quote_ctx.subscribe(stockCode, sub_type)
    ret_status, ret_data = quote_ctx.subscribe(stockCode, "ORDER_BOOK")
    print("* get_order_book : {}\n".format(quote_ctx.get_order_book(stockCode)))
    print("* get_cur_kline : {}\n".format(quote_ctx.get_cur_kline(stockCode, 10, sub_type)))
    sleep(10)
    quote_ctx.close()
