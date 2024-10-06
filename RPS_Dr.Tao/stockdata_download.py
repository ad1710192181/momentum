import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
from pandas import DataFrame

ts.set_token('194db43908c0e873e24a492a90e0d0f6157b79fa6204718377796b1e')
pro = ts.pro_api()

def data_download():
    trading_day=latest_trading_day()[0]
    #today = datetime.strptime("20240830", "%Y%m%d")

    # df_new = pro.daily(trade_date=trading_day)
    # 拼接'.csv'
    # 拉取数据
    df = pro.stock_basic(**{
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
        "symbol",   #optimizable
        "name",
        "industry",
        "market",
        #"list_status",  useless
        "list_date"
    ])   
    #filename = f"{latest_trading_day()[1]}_raw_data.csv"
    #df.to_csv(filename, index=False)


    # 示例黑名单列表
    #blacklist = ['海印股份','鹏都农牧','普利制药','波长光电','儒竞科技','多浦乐','众辰科技','泰凌微']
    blacklist = ['海印股份','普利制药',"中国重工","中国船舶"]
    #如今股份是2023年8月30日上市的
    #301528.SZ,301528,多浦乐,电器仪表,创业板,2023-08-28
    #603275.SH,603275,众辰科技,电器仪表,主板,2023-08-23
    #泰凌微
    #哈森股份 停牌5天

    # 将 list_date 转换为日期格式
    df['list_date'] = pd.to_datetime(df['list_date'], format="%Y%m%d")

    df_filtered = df[
        ~df['market'].str.contains('北交所', na=False) & 
        ~df['name'].str.contains('ST', na=False)  & 
        ~df['name'].str.contains('|'.join(blacklist), na=False) &
        (df['list_date'] < (trading_day - timedelta(days=400))) #365过于拟合250日交易日
    ]

    circ_mv = pro.daily_basic(**{
        "ts_code": "",
        "trade_date": latest_trading_day()[1],    #latest_trading_day()[1],
        "start_date": "",
        "end_date": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "total_mv",
        "circ_mv",
        "close",
        "turnover_rate",
        "turnover_rate_f"
    ])

    merged_df = pd.merge(df_filtered, circ_mv[['ts_code', 'circ_mv']], on='ts_code', how='left')
    df_filtered = merged_df[merged_df['circ_mv'] >= 100000]

    filtered_name = f"{latest_trading_day()[1]}_filtered_data.csv"
    df_filtered.to_csv(filtered_name, index=False)
    return True


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


def Stock_filter():
    
    #print(trading_day)
    df = pro.daily_basic(**{
        "ts_code": "",
        "trade_date": '20240903',    #latest_trading_day()[1],
        "start_date": "",
        "end_date": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "total_mv",
        "circ_mv",
        "close",
        "turnover_rate",
        "turnover_rate_f"
    ])
    df1= pd.read_csv('2024-09-02 00:00:00_filtered_data.csv')
    merged_df = pd.merge(df1, df[['ts_code', 'circ_mv']], on='ts_code', how='left')
    filtered_df = merged_df[merged_df['circ_mv'] >= 500000]
    filtered_df.to_csv("ozrtest111.csv", index=False)
    #print(df["circ_mv"][1])
    return True


def data_download_opt(trading_days_lookback=400, circ_mv_threshold=100000, blacklist=None):
    """
    下载并过滤股票基础数据，剔除不符合条件的记录，最终保存为 CSV 文件。

    :param trading_days_lookback: 回溯天数，默认为400
    :param circ_mv_threshold: 流通市值的下限，默认为100000
    :param blacklist: 股票黑名单列表，默认为一组预定义的值
    :return: 布尔值，表示函数是否成功执行
    """
    # 默认黑名单
    if blacklist is None:
        blacklist = ['海印股份', '普利制药', "中国重工", "中国船舶"]

    try:
        # 获取最新交易日
        trading_day = latest_trading_day()[0]

        # 拉取基础股票数据
        df = pro.stock_basic(
            ts_code="",
            name="",
            exchange="",
            market="",
            is_hs="",
            list_status="",
            limit="",
            offset="",
            fields=["ts_code", "symbol", "name", "industry", "market", "list_date"]
        )

        # 转换上市日期为日期格式
        df['list_date'] = pd.to_datetime(df['list_date'], format="%Y%m%d")

        # 过滤股票
        df_filtered = df[
            ~df['market'].str.contains('北交所', na=False) &
            ~df['name'].str.contains('ST', na=False) &
            ~df['name'].str.contains('|'.join(blacklist), na=False) &
            (df['list_date'] < (trading_day - timedelta(days=trading_days_lookback)))
        ]

        # 拉取流通市值数据
        circ_mv = pro.daily_basic(
            ts_code="",
            trade_date=latest_trading_day()[1],
            start_date="",
            end_date="",
            limit="",
            offset="",
            fields=["ts_code", "trade_date", "total_mv", "circ_mv", "close", "turnover_rate", "turnover_rate_f"]
        )

        # 合并数据并根据流通市值阈值过滤
        merged_df = pd.merge(df_filtered, circ_mv[['ts_code', 'circ_mv']], on='ts_code', how='left')
        df_filtered = merged_df[merged_df['circ_mv'] >= circ_mv_threshold]

        # 保存结果为 CSV 文件
        filtered_name = f"{latest_trading_day()[1]}_filtered_data2.csv"
        df_filtered.to_csv(filtered_name, index=False)
        
        return True

    except Exception as e:
        print(f"Error occurred: {e}")
        return False

    


if __name__ == "__main__":
    #latest_trading_day()
    print(latest_trading_day()[0],latest_trading_day()[1])
    #print((latest_trading_day() - timedelta(days=365)))

    #data_download()
    data_download_opt()
    #Stock_filter()
