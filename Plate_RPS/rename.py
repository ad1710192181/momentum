import pandas as pd


if __name__ == "__main__":

    sw = pd.read_csv('SW2021.csv')
    df_stock = pd.read_csv('filtered_stock.csv')
    ts_code_series = df_stock['ts_code']

    count = 0 

    for plate_name in sw['industry_name']:
        #print(plate_name)
        plate_name = f"Plate (copy)/{plate_name}.csv"  # 使用 f-string 创建文件名
        print(plate_name)
        df = pd.read_csv(plate_name)
        df.rename(columns={'PC50': 'PC10', 'PC120': 'PC20', 'PC250': 'PC60'}, inplace=True)
        # 检查 DataFrame 的行数
        #print(df)
        #df = df.drop(index=[1])  # 删除第二行 (索引为1)
        
        df.to_csv(plate_name, index=False)
        #for code in df['ts_code']:


    