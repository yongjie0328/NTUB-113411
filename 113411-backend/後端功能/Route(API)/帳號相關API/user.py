from fastapi import APIRouter, HTTPException, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from service import db, user
from typing import Optional
import mysql.connector
import urllib.parse

router = APIRouter(prefix="/USER", tags=['user'])

class BaseUserModel(BaseModel):
    account: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    gender: Optional[str] = None
    verification_code: Optional[str] = None

# 註冊頁面
# 1.把資料填好後，按下註冊按鈕，會先去判斷帳號是否存在
# 1-1.若帳號存在，會顯示"該帳號已存在，請選擇其他帳號"
# 1-2.若帳號不存在，會執行新增資料的動作，並顯示"帳號已成功註冊"
@router.post("/register", summary="使用者註冊帳號")
async def register_user_account(register_data: BaseUserModel):
    try:
        # 檢查帳號是否已存在
        account_exists = await db.fetch_data("user_account", "account", register_data.account)
        if account_exists:
            return {"message": "該帳號已存在，請選擇其他帳號"}

        # 執行帳號註冊
        await db.insert_data("user_account", ["account", "email", "password", "gender"], (
                            register_data.account, register_data.email, register_data.password, register_data.gender))
        
        return {"message": "帳號已成功註冊"}
    except mysql.connector.Error as db_error:
        raise HTTPException(status_code=500, detail=f"資料庫錯誤: {str(db_error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"註冊失敗: {str(e)}")

# 登入頁面
# 1.把帳號跟密碼填好後，按下登入按鈕，會先去判斷帳號是否存在
# 1-1.若帳號存在，會顯示"登入成功"，並進入首頁
# 1-2.若帳號不存在，會顯示"帳號或密碼錯誤，請重新輸入"
@router.post("/login", summary="使用者登入帳號")
async def login_user_account(login_data: BaseUserModel):
    try:
        # 檢查帳號跟密碼是否已存在
        account_exists = await user.check_account_and_password_exists("user_account", "account", "password", 
                                                                      login_data.account, login_data.password)
        if account_exists:
            # 設置cookie保存用戶帳號訊息
            encoded_account = urllib.parse.quote(login_data.account)
            response = JSONResponse(content={"message": "登入成功"})
            response.set_cookie(key="user_account", value=encoded_account)
            return response

        else:
            # 帳號不存在或密碼錯誤，返回訊息
            return {"message": "帳號或密碼錯誤，請重新輸入"} #該帳號不存在，請輸入不同的帳號或註冊新的帳號

    except Exception as e:
        # 捕捉所有其他異常，返回500錯誤
        raise HTTPException(status_code=500, detail="登入時發生錯誤：" + str(e))

# 忘記密碼頁面
# 1.使用者填寫註冊時使用的信箱，點擊提交按鈕，會先判端該信箱是否存在
# 1-1 存在的話會發送重設密碼用的驗證碼郵件至信箱裡，並且將驗證碼存入資料庫裡供比對用
@router.post("/forgot-password", summary="忘記密碼")
async def forgot_password(forgot_data: BaseUserModel):
    try:
        # 檢查信箱是否存在
        user_data = await user.check_email_exists("user_account", "email", forgot_data.email)
        if not user_data:
            return {"message": "該信箱未註冊"}

        # 發送重設密碼郵件
        verification_code = await user.send_password_reset_email(forgot_data.email)

        await user.insert_verification_code("user_account", verification_code , forgot_data.email)

        return {"message": "重設密碼郵件已發送至您的信箱，請檢查並跟隨步驟重設密碼。"}

    except mysql.connector.Error as db_error:
        raise HTTPException(status_code=500, detail=f"資料庫錯誤: {str(db_error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"發送重設密碼郵件失敗: {str(e)}")

@router.post("/Verify-verification_code", summary="驗證驗證碼")
async def Verify_verification_code(verify_data: BaseUserModel):
    try:
        is_valid = await user.check_verification_code(verify_data.verification_code)
        if not is_valid:
            raise HTTPException(status_code=400, detail="驗證碼無效或已過期")

        return {"message": "驗證碼有效，請繼續重設密碼。"}
    
    except mysql.connector.Error as db_error:
        raise HTTPException(status_code=500, detail=f"資料庫錯誤: {str(db_error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"驗證碼驗證失敗: {str(e)}")

@router.post("/reset-password", summary="重設密碼")
async def reset_password(reset_data: BaseUserModel):
    try:
        # 驗證驗證碼
        is_valid = await user.check_verification_code("user_account", reset_data.email, reset_data.verification_code)
        if not is_valid:
            raise HTTPException(status_code=400, detail="驗證碼無效或已過期")

        # 更新密碼
        await user.update_password("user_account", reset_data.account, reset_data.password)

        return {"message": "密碼重設成功"}
    except mysql.connector.Error as db_error:
        raise HTTPException(status_code=500, detail=f"資料庫錯誤: {str(db_error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重設密碼失敗: {str(e)}")

@router.get("/data", summary="獲取指定使用者的資訊")
async def get_user(user_account: str = Cookie(None), table_name: str = "user_account"):
    if user_account is None:
        raise HTTPException(status_code=400, detail="缺少帳號資料")

    try:
        # 使用Cookie中的帳號訊息來獲取使用者的資訊
        user_account_decoded = urllib.parse.unquote(user_account)
        user_info = await user.fetch_row_by_account(table_name, user_account_decoded)
        if user_info:
            return {'content': user_info}
        else:
            raise HTTPException(status_code=404, detail="未找到使用者資料") 
    except mysql.connector.Error as db_error:
        print(f"Database fetch error: {str(db_error)}")
        raise HTTPException(status_code=500, detail=f"資料庫錯誤: {str(db_error)}")
    except Exception as e:
        print(f"Exception during request handling: {str(e)}")
        raise HTTPException(status_code=500, detail=f"獲取訊息時發生錯誤: {str(e)}")

@router.patch("/update-info", summary="修改個人資訊")
async def update_user_info(update_data: BaseUserModel, user_account: str = Cookie(None)):
    if user_account is None:
        raise HTTPException(status_code=400, detail="缺少帳號資料")
    try:
        # 更新使用者資訊
        updated_info = {}
        # 用於儲存更新的內容
        updated_content = []  

        if update_data.account:
            updated_info["account"] = update_data.account
            updated_content.append('account')
        if update_data.password:
            updated_info["password"] = update_data.password
            updated_content.append('password')
        if update_data.gender:
            updated_info["gender"] = update_data.gender
            updated_content.append('gender')

        if not updated_info:
            raise HTTPException(status_code=400, detail="沒有提供要更新的資訊")
        
        user_account_decoded = urllib.parse.unquote(user_account)
        print(f"Updating user account: {user_account_decoded} with data: {updated_info}")
        
        # 執行更新操作
        await db.update_data("user_account", updated_info, "account", user_account_decoded)

        return {"message": f"{updated_info}個人資訊已成功更新", "updated_info": updated_info}
    
    except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"資料庫錯誤: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新個人資訊失敗: {str(e)}")