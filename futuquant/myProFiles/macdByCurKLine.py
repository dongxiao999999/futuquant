import pandas as pd
import futuquant as ft
import numpy as np
import datetime
import time

from futuquant.myProFiles import stockData

quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
# 获取数据
df = stockData.getCurKlines(quote_ctx, "HK.00700", "K_5M", 100)
# df.columns = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume', 'turnover']
df = df[['close', 'time_key']]


# df.head()
def get_EMA(df, N):
    for i in range(len(df)):
        if i == 0:
            df.ix[i, 'ema'] = df.ix[i, 'close']
        if i > 0:
            df.ix[i, 'ema'] = (2 * df.ix[i, 'close'] + (N - 1) * df.ix[i - 1, 'ema']) / (N + 1)
    ema = list(df['ema'])
    return ema


def get_MACD(df, short=12, long=26, M=9):
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


get_MACD(df, 12, 26, 9)
df = df[['time_key', 'dif', 'dea', 'macd', 'absMacd', 'macdRatio']]
print(df)
