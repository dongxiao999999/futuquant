import pandas as pd
import futuquant as ft
import numpy as np
import datetime
import time

quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
pre_day = '2017-05-30'
# 获取数据
# _, df = pd.read_csv('C:/Users/HXWD/Desktop/000001.csv', encoding='gbk')
_, df = quote_ctx.get_history_kline("HK.00700", start=pre_day)
df.columns = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume', 'turnover', 'change_rate']
# df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'amt']]
df = df[['close', 'time_key']]
df.head()


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
    # print(df['diff'])
    for i in range(len(df)):
        if i == 0:
            df.ix[i, 'dea'] = df.ix[i, 'diff']
        if i > 0:
            df.ix[i, 'dea'] = (2 * df.ix[i, 'diff'] + (M - 1) * df.ix[i - 1, 'dea']) / (M + 1)
    df['macd'] = 2 * (df['diff'] - df['dea'])
    return df


get_MACD(df, 12, 26, 9)
df
