from fastapi import APIRouter, HTTPException
from service import news
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

async def fetch_all_rows(table_name):
    try:
        # 每次調用時創建新的連接
        conn = create_connection()  

        # 創建游標
        cursor = conn.cursor()

        # 執行查詢
        cursor.execute(f"SELECT * FROM {table_name}")

        # 獲取所有結果
        rows = cursor.fetchall()

        # 關閉游標
        cursor.close()

        #確保在使用完後關閉連接
        conn.close()  

        return rows
    except Exception as e:
        print(f"Error fetching all rows: {e}")
        return None

# 創建路由
news_router = APIRouter(prefix="/NEWS", tags=['NEWS'])

# 新聞
# 1.獲取所有新聞資料
@news_router.get("/data", summary="瀏覽新聞")
async def browse_news(table_name:str=""):
    try:
        # 獲取所有新聞資料
        msg = await news.fetch_all_rows(table_name)
        return {'content':msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取新聞資料失敗: {str(e)}")