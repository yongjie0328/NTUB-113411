import mysql.connector
import pandas as pd

# 讀取 CSV 檔案到 DataFrame
df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_info\sii_stock_info_select.csv")

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
    "公司名稱": "company_name",
    "公司簡稱": "company_abbr",
    "產業類別": "industry_category",
    "住址": "address",
    "董事長": "chairman",
    "成立日期": "establishment_date",
    "上市日期": "sii_date",
    "普通股每股面額": "common_stock_par_value",
    "實收資本額(元)": "total_capital",
    "已發行普通股數或TDR原發行股數": "issued_common_stock",
    "編製財務報告類型": "financial_reporting_type",
    "普通股盈餘分派或虧損撥補頻率": "common_stock_dividend",
    "普通股年度(含第4季或後半年度)現金股息及紅利決議層級": "common_stock_year",
    "股票過戶機構": "stock_transfer_agent",
    "簽證會計師事務所": "certified_public_accountant",
    "英文簡稱": "english_abbr",
    "電子郵件信箱": "email",
    "公司網址": "company_website"
}

# 寫入資料到MySQL資料表
for index, row in df.iterrows():
    # 將欄位名稱對照為英文
    mapped_row = {column_mapping[key]: value for key, value in row.items()}

    # 建構寫入資料的SQL語句
    sql = "INSERT INTO sii_stock_info ({}) VALUES ({})".format(
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