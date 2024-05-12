import pandas as pd
import mysql.connector


# MySQL連線設置
host = '140.131.114.242'
port=3306
user = 'SA411'
password = '@Zxcll34ll'
database = '113-113411'

# 建立MySQL連線
conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)


async def fetch_row(table_name, col, data):
    '''

    '''
    try:
        # 創建游標
        cursor = conn.cursor()

        # 執行查詢
        cursor.execute(f"SELECT * FROM {table_name} WHERE {col} = %s", (data,))

        # 獲取結果
        row = cursor.fetchone()

        # 關閉游標
        cursor.close()

        return row
    except Exception as e:
        print(f"Error fetching row: {e}")
        return None
    
async def fetch_all_rows(table_name):
    try:
        # 創建游標
        cursor = conn.cursor()

        # 執行查詢
        cursor.execute(f"SELECT * FROM {table_name}")

        # 獲取所有結果
        rows = cursor.fetchall()

        # 關閉游標
        cursor.close()

        return rows
    except Exception as e:
        print(f"Error fetching all rows: {e}")
        return None
    
async def insert_data(table_name, cols, data):
    try:
        # 創建游標
        cursor = conn.cursor()

        # 建立 SQL 插入語句
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({','.join(['%s'] * len(data))})"

        # 執行插入
        cursor.execute(sql, data)

        # 提交事務
        conn.commit()

        # 關閉游標
        cursor.close()

        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
