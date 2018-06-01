from futuquant.open_context import *


def getStockInfoRealTime(quote_ctx, stockCode, stockList=None):
    # 首先要订阅行情
    if stockList is not None:
        for stk_code in stockList:
            ret_status, ret_data = quote_ctx.subscribe(stk_code, "QUOTE")
            if ret_status != RET_OK:
                print("%s %s: %s" % (stk_code, "QUOTE", ret_data))
                exit()
    else:
        ret_status, ret_data = quote_ctx.subscribe(stockCode, "QUOTE")
        if ret_status != RET_OK:
            print("%s %s: %s" % (stockCode, "QUOTE", ret_data))
            exit()
    ret_status, ret_data = quote_ctx.query_subscription()
    if ret_status == RET_ERROR:
        print(ret_status)
        exit()
    if stockList is not None:
        ret_status, ret_data = quote_ctx.get_stock_quote([stockList])
    else:
        ret_status, ret_data = quote_ctx.get_stock_quote([stockCode])
    if ret_status == RET_ERROR:
        print(ret_data)
        exit()
    return ret_data
