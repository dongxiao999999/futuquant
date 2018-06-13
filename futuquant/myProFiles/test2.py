from futuquant import *
from pandas import *
import pandas as pd
tradehk_ctx = OpenHKTradeContext()
pwd_unlock = '3e561a1dfebb30cc7a99d083ac75706a'
# print(tradehk_ctx.unlock_trade(password=455666, password_md5=pwd_unlock)) 正式环境需解锁
ret_code, ret_data = tradehk_ctx.position_list_query(strcode='HK.00700', stocktype='', pl_ratio_min='', pl_ratio_max='',
                                                     envtype=1)
# ret_data.ix[0]['pl_ratio']
if ret_data.empty is False:
    print("hello world")
print(ret_data)


quote_ctx = OpenQuoteContext()  # 创建行情api query_subscription()

print(quote_ctx.query_subscription())
