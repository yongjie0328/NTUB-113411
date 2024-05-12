from fastapi import APIRouter, HTTPException
import mysql.connector
from service import db


router = APIRouter(prefix="/OTC")


@router.get("/alldata")
async def get_users(table_name:str='otc_stock_info'):
    msg = await db.fetch_all_rows(table_name)
    return {'content':msg}
