import tushare as ts
import pandas as pd
#from datetime import datetime, timedelta
from pandas import DataFrame
import datetime
from dateutil.relativedelta import relativedelta

ts.set_token('...')
pro = ts.pro_api()


def individual_stock_analysis(code : str):
    
    today=datetime.date.today().strftime('%Y%m%d')
    # 计算1年2个月前的日期
    date_1_year_2_months_ago = datetime.date.today() - relativedelta(years=1, months=2)
    # 返回结果，以YYYYMMDD的形式
    stday = date_1_year_2_months_ago.strftime('%Y%m%d')

    df = pro.query('daily', ts_code=code, start_date=stday, end_date=today)
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

    data_dict = {
        "MA120": MA120,  # 可以根据需要填入具体值
        "MA250": MA250,
        "PC50":  Price_Change50,
        "PC120": Price_Change120,  # 可以根据需要填入具体值
        "PC250": Price_Change250
    }
    print(code)
    return data_dict


def RPS_compute(stock_table: pd.DataFrame):
    # 提取相关列
    ts_code_series = stock_table['ts_code']
    ts_name_series = stock_table['name']
    ts_industry_series = stock_table['industry']

    # 创建一个 DataFrame 用于存放分析结果
    results = []

    # 遍历股票代码进行分析
    for ts_code, name, industry in zip(ts_code_series, ts_name_series, ts_industry_series):
        tmp = individual_stock_analysis(ts_code)
        results.append([ts_code, name, industry, tmp['MA120'], tmp['MA250'], tmp['PC50'], tmp['PC120'], tmp['PC250']])

    # 创建结果 DataFrame
    RPS_table = pd.DataFrame(results, columns=['ts_code', 'name', 'industry', 'MA120', 'MA250', 'PC50', 'PC120', 'PC250'])
    
    total = RPS_table.shape[0]

    # 计算 RPS 排名
    RPS_table['50RPS_Rank'] = RPS_table['PC50'].rank(method='min', ascending=False)
    RPS_table['120RPS_Rank'] = RPS_table['PC120'].rank(method='min', ascending=False)
    RPS_table['250RPS_Rank'] = RPS_table['PC250'].rank(method='min', ascending=False)

    # 计算 RPS 百分比
    RPS_table['50RPS']  = round((1 - (RPS_table['50RPS_Rank']  - 1) / (total - 1)) * 100, 2)
    RPS_table['120RPS'] = round((1 - (RPS_table['120RPS_Rank'] - 1) / (total - 1)) * 100, 2)
    RPS_table['250RPS'] = round((1 - (RPS_table['250RPS_Rank'] - 1) / (total - 1)) * 100, 2)

    # 将结果保存到 CSV 文件
    RPS_table.to_csv('ozr_RPS_test.csv', index=False)

    # 将结果保存到 xlsx 文件
    #RPS_table.to_excel('ozr_test.xlsx', index=False)

def RPS_compute2(stock_table: pd.DataFrame):
    return 1



if __name__ == "__main__":
    # df_all= pd.read_csv('20240905_Filtered_stock.csv')


    # RPS_compute(df_all)
    


    df= pd.read_csv('ozr_RPS_test.csv')
    # 计算总和
    df['Total_RPS'] = df['50RPS'] + df['120RPS'] + df['250RPS']
    # 保留 Total_RPS 两位小数
    df['Total_RPS'] = df['Total_RPS'].round(2)

    # 过滤掉总和小于 255 的行
    filtered_df = df[df['Total_RPS'] >= 255]
    # 按照 Total_RPS 从大到小排序
    sorted_df = filtered_df.sort_values(by='Total_RPS', ascending=False)

    sorted_df.to_csv('ozr_RPS_test2.csv', index=False)
    #ts_code_series = df_all['ts_code']
    #ts_name_series = df_all['name']
    #print(individual_stock_analysis('002634.SZ'))
#print(datetime.date.today().strftime('%Y%m%d'))
    #kk=individual_stock_analysis('605499.SH')
    #print(kk)
    #bb=individual_stock_analysis('301421.SZ')
    #print(bb)
    # 使用 append 添加一行数据
    # 初始化空 DataFrame
    #exit(0)


