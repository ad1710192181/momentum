import csv
from bs4 import BeautifulSoup


def read_html_table_and_save_as_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table')  # 找到第一个表格

    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # 提取表格数据并写入CSV
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            data = [col.get_text(strip=True) for col in cols]
            if data:  # 只写入非空行
                writer.writerow(data)

# 使用示例
read_html_table_and_save_as_csv('stock_portfolio/2024-09-19基金持股.xls', 'stock_portfolio/output1.csv')
read_html_table_and_save_as_csv('stock_portfolio/2024-09-19北向资金.xls', 'stock_portfolio/output2.csv')
