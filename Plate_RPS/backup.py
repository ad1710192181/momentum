# 导入tushare
import tushare as ts
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
# 初始化pro接口
pro = ts.pro_api('194db43908c0e873e24a492a90e0d0f6157b79fa6204718377796b1e')



def latest_trading_day():
    # 获取当前时间
    now = datetime.now()
    today = now.date()
    current_time = now.time()

    # 定义开盘时间
    market_open_time = datetime.strptime('09:30', '%H:%M').time()

    if current_time < market_open_time:
        # 如果当前时间早于开盘时间，返回上一个交易日
        if today.weekday() == 0:  # 星期一
            latest_day = today - timedelta(days=3)  # 上一个星期五
        elif today.weekday() == 1:  # 星期二
            latest_day = today - timedelta(days=1)  # 上一个交易日
        elif today.weekday() == 2:  # 星期三
            latest_day = today - timedelta(days=1)  # 上一个交易日
        elif today.weekday() == 3:  # 星期四
            latest_day = today - timedelta(days=1)  # 上一个交易日
        elif today.weekday() == 4:  # 星期五
            latest_day = today - timedelta(days=1)  # 上一个交易日
        elif today.weekday() == 5:  # 星期六
            latest_day = today - timedelta(days=1)  # 上一个星期五
        elif today.weekday() == 6:  # 星期天
            latest_day = today - timedelta(days=2)  # 上一个星期五
    else:
        # 如果已经过了开盘时间，正常返回今天
        if today.weekday() == 5:  # 星期六
            latest_day = today - timedelta(days=1)  # 上一个星期五
        elif today.weekday() == 6:  # 星期天
            latest_day = today - timedelta(days=2)  # 上一个星期五
        else:
            latest_day = today  # 工作日则为今天

    return datetime.combine(latest_day, datetime.min.time()), latest_day.strftime('%Y%m%d')


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
    #Price_Change250=((df['close'][0]-df['close'][249])/df['close'][249]).round(5)
    #print(Price_Change120)

    data_dict = {
        "MA120": MA120,  # 可以根据需要填入具体值
        "MA250": MA250,
        "PC50":  Price_Change50,
        "PC120": Price_Change120,  
        #"PC250": Price_Change250,
    }
    print(code)
    return data_dict


if __name__ == "__main__":
    # 拉取数据
    #print(df)
    sw = pd.read_csv('SW2021.csv')
    df_stock = pd.read_csv('filtered_stock.csv')
    ts_code_series = df_stock['ts_code']

    #print(ts_code_series)
    
    count = 0 

    # 定义表头
    #columns = ["l1_code", "l1_name", "l2_code", "l2_name", "l3_code", "l3_name", "ts_code", "name", "in_date", "out_date", "is_new","PC50","PC120","PC250"]

    # 读取数据并设置表头
    #df = pd.read_csv(data_io, header=None, names=columns)

    for plate_name in sw['industry_name']:
        #print(plate_name)
        plate_name = f"Plate (copy)/{plate_name}.csv"  # 使用 f-string 创建文件名
        print(plate_name)
        df = pd.read_csv(plate_name)
        # 检查 DataFrame 的行数
        #print(df)
        #df = df.drop(index=[1])  # 删除第二行 (索引为1)
        
        #df.to_csv(plate_name, index=False)
        for code in df['ts_code']:
            # if code not in ts_code_series.values:
            #     #print(code)
            #     df = df[~df['ts_code'].str.contains(code, na=False)]

            #     df.to_csv(plate_name, index=False)

            #print(code)
            #print(df)
            data=individual_stock_analysis(code)
            df.loc[df['ts_code'] == code, ['PC50', 'PC120']] = [data["PC50"], data["PC120"]]
            
            count += 1  # 计数器加1
            if count >= 700:  # 每700次停顿
                print("..........................Paused...............................")
                time.sleep(60)  # 暂停60秒
                print("........................Keep going.............................")
                count = 0  # 重置计
            #df.to_csv(plate_name, index=False)
        df.to_csv(plate_name, index=False)

        #individual_stock_analysis()
        # 删除包含 "(退市)" 的行
        # 删除包含 '.BJ' 的行
        # df = df[~df['ts_code'].str.contains('.BJ', na=False)]

        # df.to_csv(plate_name, index=False)

        # 保存回 CSV 文件（可选）
        #df.to_csv(plate_name, index=False)
    
        



