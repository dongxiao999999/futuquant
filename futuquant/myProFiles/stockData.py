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


def getCurKlines(quote_ctx, stockCode, ktype, num):
    """ 得到实时K线 """
    # 订阅股票的各种K线种类
    sub_type_list = ["K_1M", "K_5M", "K_15M", "K_30M", "K_60M", "K_DAY", "K_WEEK", "K_MON"]
    for sub_type in sub_type_list:
        ret_status, ret_data = quote_ctx.subscribe(stockCode, sub_type)
        if ret_status != RET_OK:
            print("%s %s: %s" % (stockCode, sub_type, ret_data))
            exit()
    ret_status, ret_data = quote_ctx.query_subscription()
    if ret_status == RET_ERROR:
        print(ret_data)
        exit()
    ret_code, ret_data = quote_ctx.get_cur_kline(stockCode, num, ktype)
    if ret_code != RET_OK:
        print("%s %s: %s" % (stockCode, ktype, ret_data))
        exit()
    return ret_data


def get_EMA(df, N):
    for i in range(len(df)):
        if i == 0:
            df.ix[i, 'ema'] = df.ix[i, 'close']
        if i > 0:
            df.ix[i, 'ema'] = (2 * df.ix[i, 'close'] + (N - 1) * df.ix[i - 1, 'ema']) / (N + 1)
    ema = list(df['ema'])
    return ema


def getMACD(df, short=12, long=26, M=9):
    a = get_EMA(df, short)
    b = get_EMA(df, long)
    df['dif'] = pd.Series(a) - pd.Series(b)
    for i in range(len(df)):
        if i == 0:
            df.ix[i, 'dea'] = df.ix[i, 'dif']
        if i > 0:
            df.ix[i, 'dea'] = (2 * df.ix[i, 'dif'] + (M - 1) * df.ix[i - 1, 'dea']) / (M + 1)
    df['macd'] = 2 * (df['dif'] - df['dea'])
    df['absMacd'] = abs(df['macd'])
    meanDf = df.mean(0)
    meanMacd = meanDf['absMacd']
    df['macdRatio'] = df['absMacd'] / meanMacd
    return df

def SMA(d, N):
    v = pd.Series(index=d.index)
    last = np.nan
    for key in d.index:
        x = d[key]
        if last == last:
            x1 = (x + (N - 1) * last) / N
        else:
            x1 = x
        last = x1
        v[key] = x1
    return v

def getKDJ(data, N1=9, N2=3, N3=3):
    low1 = data['low'].rolling(window=N1).min()
    high1 = data['high'].rolling(window=N1).max()
    rsv = (data.close - low1) / (high1 - low1) * 100
    k = SMA(rsv, N2)
    d = SMA(k, N3)
    j = k * 3 - d * 2
    data['k'] = k
    data['d'] = d
    data['j'] = j
    return data