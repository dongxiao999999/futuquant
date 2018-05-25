import futuquant as ft
import pymysql as sql
from functools import partial
from peewee import *
quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
#连接服务器

# print(quote_ctx.get_stock_basicinfo(market='SH', stock_type='STOCK'))
# print(quote_ctx.get_stock_basicinfo(market='SZ', stock_type='STOCK'))
#打印获取股票信息market: 市场标识, string，例如，”HK”，”US”；具体见市场标识说明
#第一步写入股票信息到数据库

conn = sql.connect(host='127.0.0.1', user='root', passwd="root", db='mysql')
cur = conn.cursor()
cur.execute("SELECT Host,User FROM user")
data = cur.fetchall()
# for r in cur:
#     print(r)
# print(data)
cur.close()
conn.close()

db = MySQLDatabase('mysql', user='root', passwd='root')

class Book(Model):
    author = CharField(unique=True)
    title = TextField()
    class Meta:
        database = db
Book.create_table()
book = Book(author="me55", title='Peewee is cool')
# book.save()
query = Book.delete()
query.execute()
for book in Book:
    print(book.title +"  " + book.author)

# print(quote_ctx.get_market_snapshot("SZ.300123"))
#获取市场快照 get_market_snapshot 一次性获取最近当前股票列表的快照数据（每日变化的信息），该接口对股票个数有限制，一次最多传入200只股票，频率限制每3秒一次

