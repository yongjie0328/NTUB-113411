import mysql.connector
import pandas as pd

# 讀取 CSV 檔案到 DataFrame
df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_index\otc_stock_index.csv")

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
    "時 間": "time",
    "紡纖纖維": "textile_fiber",
    "電機機械": "electrical_machinery",
    "鋼鐵工業": "steel_industry",
    "建材營造": "building_materials_construction",
    "航運業": "shipping_industry",
    "觀光餐旅": "tourism_hospitality",
    "其他": "others",
    "化學工業": "chemical_industry",
    "生技醫療": "biotech_medical",
    "半導體業": "semiconductor",
    "電腦週邊業": "computer_peripheral",
    "光電業": "optoelectronics",
    "通信網路業": "communication_network",
    "電子零組件業": "electronic_components",
    "電子通路業": "electronic_distribution",
    "資訊服務業": "information_service",
    "其他電子業": "other_electronics",
    "文化創意業": "cultural_creative",
    "綠能環保": "green_energy_environmental",
    "數位雲端": "digital_cloud",
    "居家生活": "home_living",
    "電子工業": "electronics_industry",
    "櫃買指數": "otc_index",
    "成交金額(萬元)": "transaction_amount",
    "成交張數": "transaction_volume",
    "成交筆數": "transaction_count",
    "委買筆數": "buy_orders",
    "委賣筆數": "sell_orders",
    "委買張數": "buy_volume",
    "委賣張數": "sell_volume"
}

# 寫入資料到MySQL資料表
for index, row in df.iterrows():
    # 將欄位名稱對照為英文
    mapped_row = {column_mapping[key]: value for key, value in row.items()}

    # 建構寫入資料的SQL語句
    sql = "INSERT INTO otc_stock_index ({}) VALUES ({})".format(
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