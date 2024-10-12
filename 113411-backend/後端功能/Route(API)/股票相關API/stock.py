from service.stock import stock_by_id, stock_id_info, stock_price_info, stock_financial_analysis_info
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mysql.connector
from service import db

router = APIRouter(prefix="/STOCK", tags=['stock'])

# 股票相關資料
# 1.獲取股票基本資料
# 2.獲取股票歷史價格資料
# 3.獲取股票財務分析資料

@router.get("/data_id_info", summary="獲取股票基本資料")
async def get_stock_id_info(table_name:str="",value:str=""):
    res = await stock_id_info(table_name, value)
    return {'content':res}    

@router.get("/data_price_info", summary="獲取股票歷史價格資料")
async def get_stock_price_info(table_name:str="",value:str=""):
    res = await stock_price_info(table_name, value)
    return {'content':res}  

@router.get("/data_financial_analysis_info", summary="獲取股票財務分析資料")
async def get_stock_financial_analysis_info(table_name:str="",value:str=""):
    res = await stock_financial_analysis_info(table_name, value)
    return {'content':res} 