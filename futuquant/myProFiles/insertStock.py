import pandas as pd
import sys
import futuquant as ft
import peewee
from peewee import *

quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
# 连接服务器
# pd.set_option('display.max_rows',1000)
# pd.set_option('display.max_colwidth',500)
_, table1 = quote_ctx.get_stock_basicinfo(market='SH', stock_type='STOCK')
# print(basic_info_table)
# print(quote_ctx.get_stock_basicinfo(market='SZ', stock_type='STOCK'))
_, table2 = quote_ctx.get_stock_basicinfo(market='SZ', stock_type='STOCK')

# 打印获取股票信息market: 市场标识, string，例如，”HK”，”US”；具体见市场标识说明
# RET_OK, basic_info_table = quote_ctx.get_stock_basicinfo(market='SZ', stock_type='STOCK')
_, table3 = quote_ctx.get_stock_basicinfo(market='HK', stock_type='STOCK')
_, table4 = quote_ctx.get_stock_basicinfo(market='HK', stock_type='IDX')
_, table5 = quote_ctx.get_stock_basicinfo(market='HK', stock_type='ETF')
_, table6 = quote_ctx.get_stock_basicinfo(market='HK', stock_type='WARRANT')
_, table7 = quote_ctx.get_stock_basicinfo(market='HK', stock_type='BOND')

_, table8 = quote_ctx.get_stock_basicinfo(market='US', stock_type='STOCK')

tables = [table1, table2]
# 第一步写入股票信息到数据库
# db = MySQLDatabase('lim', user='limapp', passwd='hackch', host='lim.app')
db = MySQLDatabase('stock', user='root', passwd='root', host='localhost')


class StockBasicinfo(Model):
    code = CharField()
    name = CharField()
    lot_size = IntegerField()
    stock_type = CharField()
    stock_child_type = CharField()
    owner_stock_code = CharField()
    listing_date = CharField()
    stockid = CharField()
    class Meta:
        database = db
        table_name = 'stock_basicinfo'


StockBasicinfo.create_table()
for t in tables:
    for index, row in t.iterrows():
        stockBook = StockBasicinfo(code=row["code"], name=row["name"], lot_size=row["lot_size"],
                                   stock_type=row["stock_type"], stock_child_type=row["stock_child_type"],
                                   owner_stock_code=str(row["owner_stock_code"]), listing_date=row["listing_date"],
                                   stockid=row["stockid"])
        stockBook.save()
print("stock_basicinfo 表插入完了")
# print(quote_ctx.get_market_snapshot("SZ.300123"))
# 获取市场快照 get_market_snapshot 一次性获取最近当前股票列表的快照数据（每日变化的信息），该接口对股票个数有限制，一次最多传入200只股票，频率限制每3秒一次
