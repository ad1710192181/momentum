# 导入tushare
import tushare as ts
import matplotlib.pyplot as plt
# 初始化pro接口
pro = ts.pro_api('194db43908c0e873e24a492a90e0d0f6157b79fa6204718377796b1e')


# df = pro.sf_month(start_m='201901', end_m='202408')
# #print(df)

# # 设置图形大小
# plt.figure(figsize=(12, 6))

# # 绘制 inc_month 和 stk_endval
# plt.subplot(2, 1, 1)
# plt.bar(df['month'].astype(str), df['inc_month'], color='lightblue', label='Monthly Increase')
# plt.ylabel('Monthly Increase')
# plt.title('Monthly Increase Over Time')
# plt.xticks(rotation=45)

# plt.subplot(2, 1, 2)
# plt.plot(df['month'].astype(str), df['stk_endval'], marker='o', color='orange', label='Stock End Value')
# plt.ylabel('Stock End Value')
# plt.xlabel('Month')
# plt.title('Stock End Value Over Time')
# plt.xticks(rotation=45)

# # 显示图例
# plt.tight_layout()
# plt.legend()
# plt.show()
df = pro.cn_cpi(start_m='202001', end_m='202409', fields='month,nt_val,nt_yoy,nt_mom')
# 设置图形大小
plt.figure(figsize=(12, 8))

# nt_val 的柱状图
plt.subplot(3, 1, 1)
plt.bar(df['month'].astype(str), df['nt_val'], color='lightblue', label='nt_val', alpha=0.8)
plt.ylabel('nt_val')
plt.title('nt_val Over Time')
plt.xticks(rotation=45)

# nt_yoy 和 nt_mom 的折线图
plt.subplot(3, 1, 2)
plt.plot(df['month'].astype(str), df['nt_yoy'], marker='o', color='orange', label='nt YoY', linestyle='--')
plt.plot(df['month'].astype(str), df['nt_mom'], marker='o', color='green', label='nt MoM', linestyle='--')
plt.ylabel('Percentage (%)')
plt.title('nt YoY and MoM Over Time')
plt.xticks(rotation=45)
plt.legend()

# 调整布局
plt.tight_layout()
plt.show()



