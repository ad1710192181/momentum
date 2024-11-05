
from datetime import datetime, timedelta

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


def calculate_FID(df, Price_Change250):
    # 只选取前250行
    df_subset = df.head(250)
    
    # 计算收盘价差
    difference = df_subset['close'] - df_subset['pre_close']
    
    # 计算上涨和下跌的数量
    UpC_num = (difference > 0).sum()
    DownC_num = (difference < 0).sum()
    
    # 计算FID
    if Price_Change250 > 0:
        FID = round((UpC_num - DownC_num) * Price_Change250, 3)
    else:
        FID = -9999
    
    return FID