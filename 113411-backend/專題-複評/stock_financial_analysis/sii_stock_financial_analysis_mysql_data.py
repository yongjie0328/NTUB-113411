import mysql.connector
import pandas as pd

# 讀取 CSV 檔案到 DataFrame
df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_financial_analysis\sii_stock_financial_analysis_filtered.csv")

# MySQL連線設置
host = '140.131.114.242'
port=3306
user = 'SA411'
password = '@Zxcll34ll'
database = '113-113411'

# 建立MySQL連線
conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)

# 創建一個MySQL cursor物件
cursor = conn.cursor()

# 定義中文到英文的欄位名稱對照
column_mapping = {
    '股票代碼': 'stock_id',
    '公司簡稱': 'company_abbr',
    '償債能力-流動比率(%)': 'debt_ratio_current',
    '償債能力-速動比率(%)': 'debt_ratio_quick',
    '償債能力-利息保障倍數(%)': 'debt_ratio_interest_coverage',
    '經營能力-應收款項週轉率(次)': 'operating_receivables_turnover',
    '經營能力-平均收現日數': 'operating_avg_collection_days',
    '經營能力-存貨週轉率(次)': 'operating_inventory_turnover',
    '經營能力-平均售貨日數': 'operating_avg_sales_days',
    '經營能力-不動產、廠房及設備週轉率(次)': 'operating_fixed_assets_turnover',
    '經營能力-總資產週轉率(次)': 'operating_total_assets_turnover',
    '獲利能力-資產報酬率(%)': 'profitability_return_on_assets',
    '獲利能力-權益報酬率(%)': 'profitability_return_on_equity',
    '獲利能力-稅前純益佔實收資本比率(%)': 'profitability_pre_tax_net_income_to_capital',
    '獲利能力-純益率(%)': 'profitability_net_profit_margin',
    '獲利能力-每股盈餘(元)': 'profitability_earnings_per_share'
}

# 寫入資料到MySQL資料表
for index, row in df.iterrows():
    # 將欄位名稱對照為英文
    mapped_row = {column_mapping[key]: value for key, value in row.items()}

    # 建構寫入資料的SQL語句
    sql = "INSERT INTO stock_financial_analysis ({}) VALUES ({})".format(
        ", ".join(mapped_row.keys()), ", ".join(["%s"] * len(mapped_row))
    )
    
    # 獲取每一行的資料，並轉換為元組(數組)
    data = tuple(mapped_row.values())
    
    # 執行SQL語句
    cursor.execute(sql, data)

# 提交資料
conn.commit()

# 關閉MySQL連線
cursor.close()
conn.close()

print("資料已成功寫入到MySQL資料表中。")