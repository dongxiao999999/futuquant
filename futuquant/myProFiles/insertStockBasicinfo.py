import futuquant as ft
import pandas as pd
from sqlalchemy import create_engine

quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
# 连接服务器
# pd.set_option('display.max_rows',1000)
# pd.set_option('display.max_colwidth',500)
# _, table1 = quote_ctx.get_stock_basicinfo(market='SH', stock_type='STOCK')
# print(basic_info_table)
# print(quote_ctx.get_stock_basicinfo(market='SZ', stock_type='STOCK'))
# _, table2 = quote_ctx.get_stock_basicinfo(market='SZ', stock_type='STOCK')
# 打印获取股票信息market: 市场标识, string，例如，”HK”，”US”；具体见市场标识说明
# RET_OK, basic_info_table = quote_ctx.get_stock_basicinfo(market='SZ', stock_type='STOCK')
_, table3 = quote_ctx.get_stock_basicinfo(market='HK', stock_type='STOCK')
_, table4 = quote_ctx.get_stock_basicinfo(market='HK', stock_type='IDX')
_, table5 = quote_ctx.get_stock_basicinfo(market='HK', stock_type='ETF')
_, table6 = quote_ctx.get_stock_basicinfo(market='HK', stock_type='WARRANT')
_, table7 = quote_ctx.get_stock_basicinfo(market='HK', stock_type='BOND')
_, table8 = quote_ctx.get_stock_basicinfo(market='US', stock_type='STOCK')
# 插入港股的基本信息
tables = [table3, table4, table5, table6, table7]
engine = create_engine('mysql://root:root@localhost/stock?charset=utf8') #用sqlalchemy创建引擎
for i in range(len(tables)):
    pd.io.sql.to_sql(tables[i], 'stock_basicinfo', engine, if_exists='append')
print("stock_basicinfo 表插入完了")
# print(quote_ctx.get_market_snapshot("SZ.300123"))
# 获取市场快照 get_market_snapshot 一次性获取最近当前股票列表的快照数据（每日变化的信息），该接口对股票个数有限制，一次最多传入200只股票，频率限制每3秒一次
