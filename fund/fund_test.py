# 导入tushare
import tushare as ts
import pandas as pd

# 初始化pro接口
pro = ts.pro_api('194db43908c0e873e24a492a90e0d0f6157b79fa6204718377796b1e')

 
#df1=pro.hsgt_top10(trade_date='20240910', market_type='1')
 
#df2=pro.hsgt_top10(trade_date='20240910', market_type='3')

# df3=pro.hsgt_top10(trade_date='20240910')
# sorted_df = df3.sort_values(by='amount', ascending=False)
    
# print(sorted_df)   

def all_fund():
    # 拉取数据
    df_fund1 = pro.fund_basic(**{
        "ts_code": "",
        "market": "",
        "update_flag": "",
        "offset": "",
        "limit": "",
        "status": "L",
        "name": ""
    }, fields=[
        "ts_code",
        "name",
        "invest_type",
        "type",
        "market",
        "fund_type",
        "list_date"
    ])


    #df_fund1.to_csv('fund_all1.csv', index=False)

    # 拉取数据
    df_fund2 = pro.fund_basic(**{
        "ts_code": "",
        "market": "",
        "update_flag": "",
        "offset": "10000",
        "limit": "",
        "status": "L",
        "name": ""
    }, fields=[
        "ts_code",
        "name",
        "invest_type",
        "type",
        "market",
        "fund_type",
        "list_date"
    ])
    #df_fund2.to_csv('fund_all2.csv', index=False)
    merged_df = pd.concat([df_fund1, df_fund2]).drop_duplicates()
    merged_df.to_csv('fund_all.csv', index=False)
    return True

#df = pro.fund_portfolio(symbol='301004.SZ', start_date='20240515', end_date="20240911")
df = pro.fund_portfolio(symbol='600519.SH', start_date='20240615')
df_fund= pd.read_csv('fund_all.csv')


merged_df = pd.merge(df, df_fund[['ts_code', 'name']], on='ts_code', how='left')
merged_df.to_csv('hebin.csv', index=False)
#print(df_fund)    
#print(sorted_df)