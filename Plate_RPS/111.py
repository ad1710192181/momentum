
# 导入tushare
import tushare as ts
import pandas as pd
# 初始化pro接口
pro = ts.pro_api('194db43908c0e873e24a492a90e0d0f6157b79fa6204718377796b1e')




if __name__ == "__main__":

    sw = pd.read_csv('SW2021.csv')
    df_stock = pd.read_csv('filtered_stock.csv')
    #ts_code_series = df_stock['ts_code']

    
    columns = ['plate_name', 'PC10', 'PC20','PC60']
    rps = pd.DataFrame(columns=columns)
    

    for plate_name1 in sw['industry_name']:
        #print(plate_name)
        plate_name = f"Plate (pc10,20,60)/{plate_name1}.csv"  # 使用 f-string 创建文件名
        #print(plate_name)
        df = pd.read_csv(plate_name)
        mean_pc10 = df["PC10"].mean()
        mean_pc10_rounded = round(mean_pc10, 5)
        mean_pc20 = df["PC20"].mean()
        mean_pc20_rounded = round(mean_pc20, 5)
        mean_pc60 = df["PC60"].mean()
        mean_pc60_rounded = round(mean_pc60, 5)



        new_row = {
            "plate_name":plate_name1,
            "PC10": mean_pc10_rounded,
            "PC20": mean_pc20_rounded,
            "PC60": mean_pc60_rounded
        }
        #print("ok")
        rps = pd.concat([rps, pd.DataFrame([new_row])], ignore_index=True)


    total = rps.shape[0]
    rps['10RPS_Rank'] = rps['PC10'].rank(method='min', ascending=False)
    rps['20RPS_Rank'] = rps['PC20'].rank(method='min', ascending=False)
    rps['60RPS_Rank'] = rps['PC60'].rank(method='min', ascending=False)

    # 计算 RPS 百分比
    rps['10RPS']  = round((1 - (rps['10RPS_Rank']  - 1) / (total - 1)) * 100, 2)
    rps['20RPS'] = round((1 - (rps['20RPS_Rank'] - 1) / (total - 1)) * 100, 2)
    rps['60RPS'] = round((1 - (rps['60RPS_Rank'] - 1) / (total - 1)) * 100, 2)

    # 删除排名列
    rps.drop(columns=['10RPS_Rank', '20RPS_Rank', '60RPS_Rank'], inplace=True)

    rps.fillna(-999, inplace=True)
    rps = rps.sort_values(by='10RPS', ascending=False)
    
    rps.to_csv("plate_rps.csv", index=False)
    # 计算 RPS 排名
    
        



