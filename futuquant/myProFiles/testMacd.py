import pandas as pd
import futuquant as ft
import numpy as np
import datetime
import time

from futuquant.myProFiles import stockData

quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
pre_day = '2017-05-30'
# 获取数据
# _, df = pd.read_csv('C:/Users/HXWD/Desktop/000001.csv', encoding='gbk')
_, df = quote_ctx.get_history_kline("HK.00700", start=pre_day)
df.columns = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume', 'turnover',
              'change_rate']
# df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'amt']]
df = df[['close', 'time_key']]
ret_data = stockData.getStockInfoRealTime(quote_ctx, stockCode='HK.00700')
ret_data = ret_data[['last_price', 'data_date']]
# ret_data.columns = [['close', 'time_key']]
ret_data = ret_data.rename(columns={'last_price': 'close'})
ret_data = ret_data.rename(columns={'data_date': 'time_key'})
ret_data[["time_key"]] = ret_data[["time_key"]] + " 00:00:00"
df = pd.concat([df, ret_data], axis=0)
df.index = pd.Series(range(len(df)))

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
    for i in range(len(df)):
        if i == 0:
            df.ix[i, 'dea'] = df.ix[i, 'dif']
        if i > 0:
            df.ix[i, 'dea'] = (2 * df.ix[i, 'dif'] + (M - 1) * df.ix[i - 1, 'dea']) / (M + 1)
    df['macd'] = 2 * (df['dif'] - df['dea'])
    return df


get_MACD(df, 12, 26, 9)
df
