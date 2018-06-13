import numpy as np
import pandas as pd
import futuquant as ft
from futuquant.myProFiles import stockData


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

def kdj(data, N1=9, N2=3, N3=3):
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

quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
# 获取数据
df = stockData.getCurKlines(quote_ctx, "HK.00700", "K_15M", 100)
df = kdj(df, 9, 3, 3)

print(df)
