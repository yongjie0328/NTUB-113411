from fastapi import APIRouter, HTTPException, Cookie
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from service import db
import pytz

router = APIRouter(prefix="/NEWS", tags=['news'])

# 新聞
# 1.獲取所有新聞資料
@router.get("/data", summary="瀏覽新聞")
async def browse_news(table_name:str=""):
    try:
        # 獲取所有新聞資料
        msg = await db.fetch_all_rows(table_name)
        return {'content':msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取新聞資料失敗: {str(e)}")