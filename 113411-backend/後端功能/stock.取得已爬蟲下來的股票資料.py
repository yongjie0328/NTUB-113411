from fastapi import APIRouter
import mysql.connector

# 資料庫連接配置
def create_connection():
    return mysql.connector.connect(
        host='140.131.114.242',   # 資料庫IP
        port=3306,                # 端口號
        user='SA411',             # 資料庫帳號
        password='@Zxcll34ll',    # 資料庫密碼
        database='113-113411'     # 資料庫名稱
    ) 

# 獲取股票基本資料
async def stock_id_info(table_name, condition_value):
    # 每次調用時創建新的連接
    conn = create_connection()

    # 創建游標
    cursor = conn.cursor()

    # 建構查詢語句
    query = f"SELECT * FROM {table_name} WHERE stock_id = {condition_value} LIMIT 10" 

    # 執行查詢並傳入條件值
    cursor.execute(query)

    # 獲取查詢結果，並將結果儲存為字串型別的列表
    result = [row for row in cursor.fetchall()]

    # 關閉游標
    cursor.close()

    # 確保在使用完後關閉連接
    conn.close()  

    return result

# 獲取股票歷史價格資料
async def stock_price_info(table_name, condition_value):
    # 每次調用時創建新的連接
    conn = create_connection() 

    cursor = conn.cursor()

    # 建構查詢語句
    query = f"SELECT * FROM {table_name} WHERE stock_id = {condition_value} LIMIT 10" 

    # 執行查詢並傳入條件值
    cursor.execute(query)

    # 獲取查詢結果，並將結果儲存為字串型別的列表
    result = [row for row in cursor.fetchall()]

    # 關閉游標
    cursor.close()

    # 確保在使用完後關閉連接
    conn.close()  

    return result

# 獲取股票財務分析資料
async def stock_financial_analysis_info(table_name, condition_value):
    # 每次調用時創建新的連接
    conn = create_connection()  

    cursor = conn.cursor()

    # 建構查詢語句
    query = f"SELECT * FROM {table_name} WHERE stock_id = {condition_value} LIMIT 10" 

    # 執行查詢並傳入條件值
    cursor.execute(query)

    # 獲取查詢結果，並將結果儲存為字串型別的列表
    result = [row for row in cursor.fetchall()]

    # 關閉游標
    cursor.close()

    # 確保在使用完後關閉連接
    conn.close()  

    return result

# 創建路由
stock_router = APIRouter(prefix="/STOCK", tags=['STOCK'])

# 股票相關資料
# 1.獲取股票基本資料
# 2.獲取股票歷史價格資料
# 3.獲取股票財務分析資料
@stock_router.get("/data_id_info", summary="獲取股票基本資料")
async def get_stock_id_info(table_name:str="",value:str=""):
    res = await stock_id_info(table_name, value)
    return {'content':res}    

@stock_router.get("/data_price_info", summary="獲取股票歷史價格資料")
async def get_stock_price_info(table_name:str="",value:str=""):
    res = await stock_price_info(table_name, value)
    return {'content':res}  

@stock_router.get("/data_financial_analysis_info", summary="獲取股票財務分析資料")
async def get_stock_financial_analysis_info(table_name:str="",value:str=""):
    res = await stock_financial_analysis_info(table_name, value)
    return {'content':res} 