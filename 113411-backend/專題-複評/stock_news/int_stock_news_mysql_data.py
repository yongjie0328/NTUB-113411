import mysql.connector
import pandas as pd

# 讀取 CSV 檔案到 DataFrame
df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_news\int_stock_news_translated.csv")

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
    "URL": "url",
    "Title": "title",
    "Summary": "summary",
    "Keywords": "keyword",
    "Sentiment": "sentiment",
}

# 寫入資料到MySQL資料表
for index, row in df.iterrows():
    # 將欄位名稱對照為英文
    mapped_row = {column_mapping[key]: value for key, value in row.items()}

    # 建構寫入資料的SQL語句
    sql = "INSERT INTO int_stock_news ({}) VALUES ({})".format(
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