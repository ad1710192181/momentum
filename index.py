# 导入tushare
import tushare as ts
# 初始化pro接口
pro = ts.pro_api('...')

# 拉取数据
df = pro.index_basic(**{
    "ts_code": "",
    "market": "",
    "publisher": "",
    "category": "",
    "name": "",
    "limit": "",
    "offset": ""
}, fields=[
    "ts_code",
    "name",
    "market",
    "publisher",
    "category",
    "base_date",
    "base_point",
    "list_date",
    "fullname",
    "index_type",
    "desc"
])
#print(df)
filename = f"{'index'}.csv"
df.to_csv(filename, index=False)


        