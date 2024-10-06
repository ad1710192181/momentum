import tushare as ts
import pandas as pd

ts.set_token('194db43908c0e873e24a492a90e0d0f6157b79fa6204718377796b1e')
pro = ts.pro_api()

#df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
#多个股票
#df = pro.daily(ts_code='**', start_date='20180701', end_date='20180702')
#df = pro.index_basic(market='SSE')

df_new = pro.daily(trade_date='20240816')
#df = pro.new_share(start_date='20210901', end_date='20211018')
df_new.to_csv('data_new.csv', index=False)
#print(type(df))
#print(df)
#print(df["ts_code"][5])
#print(type(df["ts_code"][5]))
print("ozr")

"""
df_all = pro.stock_basic(**{
    "ts_code": "",
    "name": "",
    "exchange": "",
    "market": "",
    "is_hs": "",
    "list_status": "",
    "limit": "",
    "offset": ""
}, fields=[
    "ts_code",
    "symbol",
    "name",
    "area",
    "industry",
    "cnspell",
    "market",
    "list_date",
    "act_name",
    "act_ent_type",
    "fullname"
])
#df_all.to_csv('all_stock.csv', index=False)
#df_all.to_excel('all_stock.xlsx', index=False)
"""
