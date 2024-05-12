from fastapi import APIRouter, HTTPException
import mysql.connector
from service import db


router = APIRouter(prefix="/USER")

# 搜索資料庫結果並比對

#註冊
@router.get("/register")
async def get_users(id, password, email, gender):
    '''
    先判斷user_id是否存在，不存在的話就新增資料到資料庫裡
    '''
    table_name = "user_account"
    col = "user_id"
    name_exist = await db.fetch_row(table_name, col, id)

    user_columns = "user_id, password, email, gender"

    if name_exist:
        return {"msg":f"user:{id} is exist."}
    else:
        await db.insert_data(table_name, user_columns, (id, password, email, gender))
        return {"msg": f"user:{id} is inserted into table: {col}."}
