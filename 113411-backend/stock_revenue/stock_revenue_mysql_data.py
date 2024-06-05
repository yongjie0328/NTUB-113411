import pandas as pd
import mysql.connector

# 讀取 CSV 檔案到 DataFrame
df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_revenue\stock_revenue.csv") #要更改

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
    "股票代碼": "stock_id",
    "公司簡稱": "company_abbr",
    "當月營收(千元)": "current_month_revenue",
    "上月營收(千元)": "last_month_revenue",
    "去年當月營收(千元)": "last_year_same_month_revenue",
    "上月比較增減(%)": "month_over_month_change_percentage",
    "去年同月增減(%)": "year_over_year_change_percentage",
    "當月累計營收(千元)": "current_month_accumulated_revenue",
    "去年累計營收(千元)": "last_year_accumulated_revenue",
    "前期比較增減(%)": "year_to_date_change_percentage",
    "備註": "notes"
}

# 寫入資料到MySQL資料表
for index, row in df.iterrows():
    # 將欄位名稱對照為英文
    mapped_row = {column_mapping[key]: value for key, value in row.items()}

    # 建構寫入資料的SQL語句
    sql = "INSERT INTO stock_revenue ({}) VALUES ({})".format(
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