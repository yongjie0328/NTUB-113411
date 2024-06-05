import mysql.connector
import pandas as pd

# 讀取 CSV 檔案到 DataFrame
df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_index\sii_stock_index.csv")

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
    "時間": "time",
    "發行量加權股價指數": "weighted_stock_index",
    "未含金融保險股指數": "ex_financial_insurance_index",
    "未含電子股指數": "ex_electronics_index",
    "未含金融電子股指數": "ex_financial_electronics_index",
    "水泥類指數": "cement_index",
    "食品類指數": "food_index",
    "塑膠類指數": "plastics_index",
    "紡織纖維類指數": "textile_fiber_index",
    "電機機械類指數": "electrical_machinery_index",
    "電器電纜類指數": "electric_cable_index",
    "化學生技醫療類指數": "chemical_biotech_medical_index",
    "化學類指數": "chemical_index",
    "生技醫療類指數": "biotech_medical_index",
    "玻璃陶瓷類指數": "glass_ceramics_index",
    "造紙類指數": "paper_index",
    "鋼鐵類指數": "steel_index",
    "橡膠類指數": "rubber_index",
    "汽車類指數": "automobile_index",
    "電子類指數": "electronics_index",
    "半導體類指數": "semiconductor_index",
    "電腦及週邊設備類指數": "computer_peripheral_equipment_index",
    "光電類指數": "optoelectronics_index",
    "通信網路類指數": "communication_network_index",
    "電子零組件類指數": "electronic_components_index",
    "電子通路類指數": "electronic_distribution_index",
    "資訊服務類指數": "information_service_index",
    "其他電子類指數": "other_electronics_index",
    "建材營造類指數": "building_materials_construction_index",
    "航運類指數": "shipping_index",
    "觀光餐旅類指數": "tourism_index",
    "金融保險類指數": "financial_insurance_index",
    "貿易百貨類指數": "trade_department_store_index",
    "油電燃氣類指數": "oil_gas_electricity_index",
    "綠能環保類指數": "green_energy_environmental_index",
    "數位雲端類指數": "digital_cloud_index",
    "運動休閒類指數": "sports_leisure_index",
    "居家生活類指數": "home_living_index",
    "其他類指數": "other_index"
}

# 寫入資料到MySQL資料表
for index, row in df.iterrows():
    # 將欄位名稱對照為英文
    mapped_row = {column_mapping[key]: value for key, value in row.items()}

    # 建構寫入資料的SQL語句
    sql = "INSERT INTO sii_stock_index ({}) VALUES ({})".format(
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