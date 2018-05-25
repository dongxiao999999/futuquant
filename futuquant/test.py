import futuquant as ft

quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
#连接服务器

print(quote_ctx.get_stock_basicinfo(market='SH', stock_type='STOCK'))
# print(quote_ctx.get_stock_basicinfo(market='SZ', stock_type='STOCK'))
#打印获取股票信息market: 市场标识, string，例如，”HK”，”US”；具体见市场标识说明
#第一步写入股票信息到数据库

# print(quote_ctx.get_market_snapshot("SZ.300123"))
#获取市场快照 get_market_snapshot 一次性获取最近当前股票列表的快照数据（每日变化的信息），该接口对股票个数有限制，一次最多传入200只股票，频率限制每3秒一次

