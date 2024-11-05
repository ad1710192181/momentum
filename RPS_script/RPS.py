import tushare as ts
import pandas as pd
from pandas import DataFrame
import datetime as dt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

import matplotlib.pyplot as plt
from util import latest_trading_day,calculate_FID

ts.set_token('194db43908c0e873e24a492a90e0d0f6157b79fa6204718377796b1e')
pro = ts.pro_api()



def individual_stock_analysis(code : str):
    
    today=dt.date.today().strftime('%Y%m%d')

    # 计算1年2个月前的日期
    date_1_year_2_months_ago = dt.date.today() - relativedelta(years=1, months=2)
    # 返回结果，以YYYYMMDD的形式
    stday = date_1_year_2_months_ago.strftime('%Y%m%d')

    #df = pro.query('daily', ts_code=code, start_date=stday, end_date=today)
    df= ts.pro_bar(ts_code=code, freq='D', adj='qfq', start_date=stday, end_date=today)
    #print(df)
    
    #MA5=df['pre_close'][:5].mean().round(2)   #5day 
    #MA10=df['pre_close'][:10].mean().round(2)
    MA120=df['close'][:120].mean().round(2)
    MA250=df['close'][:250].mean().round(2)
    #print(MA5,MA10,MA120,MA250)

    Price_Change50=((df['close'][0]-df['close'][49])/df['close'][49]).round(5)
    Price_Change120=((df['close'][0]-df['close'][119])/df['close'][119]).round(5)
    Price_Change250=((df['close'][0]-df['close'][249])/df['close'][249]).round(5)
    #print(Price_Change120)


    if(df['close'][0]>MA120>MA250):
        bullMA=1
    else:
        bullMA=0

    if(df['close'][0]>(df['high'][:250].max()*0.85)):
        NewHigh=1
    else:
        NewHigh=0

    #df['high'][:250].max()
    FID=calculate_FID(df, Price_Change250)

    data_dict = {
        "MA120": MA120,  # 可以根据需要填入具体值
        "MA250": MA250,
        "PC50":  Price_Change50,
        "PC120": Price_Change120,  
        "PC250": Price_Change250,
        "FID":FID,
        "bullMA":bullMA,
        "NewHigh":NewHigh
    }
    print(code)
    #print(data_dict)
    return data_dict


def RPS_compute(stock_table: pd.DataFrame):
    # 提取相关列
    ts_code_series = stock_table['ts_code']
    ts_name_series = stock_table['name']
    ts_industry_series = stock_table['industry']
    ts__circ_mv_series = stock_table['circ_mv']//10000
    ts_turnover_series = stock_table['turnover_rate_f'].round(2)


    # 创建一个 DataFrame 用于存放分析结果
    results = []

    # 遍历股票代码进行分析
    count = 0 
    for ts_code, name, industry, circ_mv, turnover in zip(ts_code_series, ts_name_series,ts_industry_series,ts__circ_mv_series,ts_turnover_series):
        tmp = individual_stock_analysis(ts_code)
        results.append([ts_code, name, industry, circ_mv, turnover, tmp['MA120'], tmp['MA250'], tmp['PC50'], tmp['PC120'], tmp['PC250'], tmp["FID"], tmp["bullMA"], tmp["NewHigh"]])

        count += 1  # 计数器加1
        if count >= 700:  # 每700次停顿
            print("..........................Paused...............................")
            time.sleep(60)  # 暂停60秒
            print("........................Keep going.............................")
            count = 0  # 重置计数器

    # 创建结果 DataFrame
    RPS_table = pd.DataFrame(results, columns=['ts_code', 'name', 'industry', 'circ_mv', 'turnover', 'MA120', 'MA250', 'PC50', 'PC120', 'PC250','FID', 'bullMA', 'NewHigh'])
    
    total = RPS_table.shape[0]

    # 计算 RPS 排名
    RPS_table['50RPS_Rank'] = RPS_table['PC50'].rank(method='min', ascending=False)
    RPS_table['120RPS_Rank'] = RPS_table['PC120'].rank(method='min', ascending=False)
    RPS_table['250RPS_Rank'] = RPS_table['PC250'].rank(method='min', ascending=False)

    # 计算 RPS 百分比
    RPS_table['50RPS']  = round((1 - (RPS_table['50RPS_Rank']  - 1) / (total - 1)) * 100, 2)
    RPS_table['120RPS'] = round((1 - (RPS_table['120RPS_Rank'] - 1) / (total - 1)) * 100, 2)
    RPS_table['250RPS'] = round((1 - (RPS_table['250RPS_Rank'] - 1) / (total - 1)) * 100, 2)

    # 删除排名列
    RPS_table.drop(columns=['50RPS_Rank', '120RPS_Rank', '250RPS_Rank'], inplace=True)

    RPS_table.sort_values(by='250RPS', ascending=False, inplace=True)
    #RPS_table.to_csv('ozr_RPS_test.csv', index=False)
    return RPS_table



def Conditional_filtering(stock_table: pd.DataFrame):

    df1 = stock_table[stock_table["250RPS"] > 70]
    df1 = df1.sort_values(by="FID", ascending=False)

    df2 = df1[(df1['50RPS'] > 90) | (df1['120RPS'] > 90) | (df1['250RPS'] > 90)]
    #df2 = df2.sort_values(by="FID", ascending=False)

    df3 = df2[(df2['bullMA'] == 1) & (df2['NewHigh'] == 1) & (df2['turnover']<20) & (df2['circ_mv']>90)]
    #df3 = df3.sort_values(by="FID", ascending=False)

    df4 = df3[(df3['120RPS'] > 90) & (df3['250RPS'] > 90)]

    name = 'rps_' + latest_trading_day()[1] + '.xlsx'
    with pd.ExcelWriter(name) as writer:
        df1.to_excel(writer, sheet_name='RPS250>70', index=False)
        df2.to_excel(writer, sheet_name='RPS>90', index=False)
        df3.to_excel(writer, sheet_name='RPS>90plus', index=False)
        df4.to_excel(writer, sheet_name='RPS>90plusplus', index=False)
    return True


if __name__ == "__main__":

    name = 'StockPool/'+latest_trading_day()[1] + '_stocks_Drtao.csv'
    df= pd.read_csv(name)
    rps_table = RPS_compute(df)
    Conditional_filtering(rps_table)




