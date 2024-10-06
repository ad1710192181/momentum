import pandas as pd

# 加载 CSV 文件
df1 = pd.read_csv('stock_portfolio/output1.csv')
# 加载 CSV 文件
df2 = pd.read_csv('stock_portfolio/output2.csv')
# 筛选流通股东持股市值大于等于30000000的行
df2 = df2[df2['流通股东持股市值'] >= 30000000]
# 将结果写回到新的 CSV 文件
df2.to_csv('stock_portfolio/output2.csv', index=False)


meg1 = df1[['股票代码', '股票简称']]
meg2 = df2[['股票代码', '股票简称']]
# 获取交集
union_df = pd.concat([meg1, meg2]).drop_duplicates()
union_df .to_csv('stock_portfolio/intersection.csv', index=False)
# 获取并打印表头
print("表头1:", df1.columns.tolist())
# 获取并打印表头
print("表头2:", df2.columns.tolist())


