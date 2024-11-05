import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
from pandas import DataFrame
from util import latest_trading_day

ts.set_token('194db43908c0e873e24a492a90e0d0f6157b79fa6204718377796b1e')
pro = ts.pro_api()


def data_download_tao(trading_days_lookback=400, circ_mv_threshold=300000, blacklist=None):
    """
    下载并过滤股票基础数据，剔除不符合条件的记录，最终保存为 CSV 文件。

    :param trading_days_lookback: 回溯天数，默认为400
    :param circ_mv_threshold: 流通市值的下限，默认为100000
    :param blacklist: 股票黑名单列表，默认为一组预定义的值
    :return: 布尔值，表示函数是否成功执行
    """
    # 默认黑名单
    if blacklist is None:
        blacklist = ['海印股份', '普利制药']

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
            #trade_date='20240930',
            start_date="",
            end_date="",
            limit="",
            offset="",
            fields=["ts_code", "trade_date", "total_mv", "circ_mv", "close", "turnover_rate", "turnover_rate_f"]
        )

        # 合并数据并根据流通市值阈值过滤
        merged_df = pd.merge(df_filtered, circ_mv[['ts_code', 'circ_mv', 'turnover_rate_f']], on='ts_code', how='left')
        df_filtered = merged_df[merged_df['circ_mv'] >= circ_mv_threshold]


        df_tao = pd.read_csv('StockPool/intersection.csv')
        df_filtered = df_filtered[df_filtered['ts_code'].isin(df_tao['ts_code'])]

        # 保存结果为 CSV 文件
        filtered_name = f"StockPool/{latest_trading_day()[1]}_stocks_Drtao.csv"
        df_filtered.to_csv(filtered_name, index=False)
        
        return True

    except Exception as e:
        print(f"Error occurred: {e}")
        return False    


if __name__ == "__main__":
    data_download_tao()


