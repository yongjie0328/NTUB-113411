from fastapi import APIRouter, HTTPException, Cookie
from email.mime.multipart import MIMEMultipart
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Optional
import mysql.connector
from service import user
import urllib.parse
import smtplib
import random
import string

# 資料庫連接配置
def create_connection():
    return mysql.connector.connect(
        host='140.131.114.242',   # 資料庫IP
        port=3306,                # 端口號
        user='SA411',             # 資料庫帳號
        password='@Zxcll34ll',    # 資料庫密碼
        database='113-113411'     # 資料庫名稱
    ) 

async def check_account_and_password_exists(table_name, account_col, password_col, account, password):
    try:
        # 每次調用時創建新的連接
        conn = create_connection()  

        # 創建游標
        cursor = conn.cursor()

        # 執行查詢
        cursor.execute(f"SELECT * FROM {table_name} WHERE {account_col} = %s AND {password_col} = %s", (account, password))

        # 獲取結果
        row = cursor.fetchone()

        # 關閉游標
        cursor.close()

        #確保在使用完後關閉連接
        conn.close()  

        return row
    except Exception as e:
        print(f"獲取資料時發生錯誤：{e}")
        return None

async def check_account_exists(table_name, account_col, account):
    try:
        # 每次調用時創建新的連接
        conn = create_connection()  

        # 創建游標
        cursor = conn.cursor()

        # 執行查詢
        cursor.execute(f"SELECT * FROM {table_name} WHERE {account_col} = %s", (account,))

        # 獲取結果
        row = cursor.fetchone()

        # 關閉游標
        cursor.close()

        conn.close()  # 确保在使用完后关闭连接

        return row is not None  # 如果找到了該帳號，返回 True；否則返回 False
    except Exception as e:
        print(f"獲取資料時發生錯誤：{e}")
        return False

# 在資料庫中儲存驗證碼
async def store_verification_code(email, verification_code):
    try:
        # 每次調用時創建新的連接
        conn = create_connection()  

        # 創建游標
        cursor = conn.cursor()

        # 建構查詢語句
        sql = f"INSERT INTO verification_codes (email, verification_code) VALUES (%s, %s)", (email, verification_code)
        
        # 執行插入
        cursor.execute(sql,(email, verification_code))

        # 提交事務
        conn.commit()

        # 關閉游標
        cursor.close()

        #確保在使用完後關閉連接
        conn.close()  

        print("Verification code stored successfully.")
    except Exception as e:
        print(f"Error storing verification code: {e}")

async def check_verification_code(verification_code):
    try:
        #  每次調用時創建新的連接
        conn = create_connection()  

        # 創建游標
        cursor = conn.cursor()

        # 建構查詢語句
        cursor.execute("SELECT * FROM verification_codes WHERE verification_code = %s", (verification_code,))

        # 獲取結果
        row = cursor.fetchone()

        # 關閉游標
        cursor.close()

        #確保在使用完後關閉連接
        conn.close()  

        # 返回結果，若存在則返回 True，否則返回 False
        return row is not None
    except Exception as e:
        print(f"獲取資料時發生錯誤：{e}")
        # return False
        return None

async def check_email_exists(table_name, email_col, email):
    try:
        # 每次調用時創建新的連接
        conn = create_connection()  

        # 創建游標
        cursor = conn.cursor()

        # 建構查詢語句
        cursor.execute(f"SELECT * FROM {table_name} WHERE {email_col} = %s", (email,))

        # 獲取結果
        row = cursor.fetchone()

        # 關閉游標
        cursor.close()

        # 確保在使用完後關閉連接
        conn.close() 

        return row is not None  # 如果找到了該帳號，返回 True；否則返回 False
    except Exception as e:
        print(f"獲取資料時發生錯誤：{e}")
        return False

async def update_password(table_name, enail, password):
    try:
        # 每次調用時創建新的連接
        conn = create_connection()  

        # 建立游標
        cursor = conn.cursor()

        # 建立 SQL 插入語句
        sql = f"UPDATE {table_name} SET `password` = '{password}' WHERE `account` = '{enail}'"

        # 執行更新
        cursor.execute(sql)

        # 提交事務
        conn.commit()
        print(f"Rows affected: {cursor.rowcount}")
        res = cursor.rowcount

        # 關閉游標
        cursor.close()

        conn.close()  # 确保在使用完后关闭连接

        return res
        # print("Password updated successfully.")
    except Exception as e:
        print(f"Error updating password: {e}")
        return None

async def insert_verification_code(table_name, data, email):
    try:
        conn = create_connection()  # 每次调用时创建新的连接

        # 創建游標
        cursor = conn.cursor()

        # 建立 SQL 插入語句
        # sql = f"UPDATE `{table_name}` SET `verification_code` = %s WHERE (`email` = %s)"
        sql = f"UPDATE `{table_name}` SET `verification_code` = '{data}' WHERE (`email` = '{email}')"

        # 執行新增
        # cursor.execute(sql, (data, email))
        cursor.execute(sql)

        # 提交事務
        conn.commit()

        # 關閉游標
        cursor.close()

        conn.close()  # 确保在使用完后关闭连接

        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")

async def send_password_reset_email(email):
    # 你的郵件帳號資訊
    sender_email = "test113411@gmail.com"  # 你的電子郵件地址
    password = "nhml qqup yswr sssm"  # 你的郵件密碼

    # 生成隨機驗證碼
    def generate_verification_code(length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    verification_code = generate_verification_code()

    # 信件主題
    subject = "Password Reset Request"

    # 信件內容
    message = MIMEMultipart()
    message["From"] = formataddr(("", sender_email))  # 修改這一行
    message["To"] = email
    message["Subject"] = subject

    # 密碼重置郵件內容，這裡可以自定義郵件內容
    body = f"您收到此郵件是因為您（或者有人冒充您）申請了密碼重置。如果這不是您的操作，請忽略此郵件。\n\n如果是您的操作，請使用以下驗證碼重置您的密碼：\n\n驗證碼： {verification_code}\n\n此驗證碼將在24小時內失效。\n\n感謝您的使用！"
    message.attach(MIMEText(body, "plain"))

    # 連接郵件服務器
    with smtplib.SMTP("smtp.gmail.com", 587) as server:  # 修改成你的郵件服務器地址和端口
        server.starttls()  # 啟用 TLS
        server.login(sender_email, password)  # 登錄到郵件服務器
        server.sendmail(sender_email, email, message.as_string())  # 發送郵件
    return verification_code  # 返回生成的驗證碼，這樣你可以在其他地方使用

async def fetch_row_by_account(table_name, account):
    try:
        conn = create_connection()  # 每次调用时创建新的连接

        # 創建游標
        cursor = conn.cursor()

        # 建構查詢語句
        cursor.execute(f"SELECT * FROM {table_name} WHERE account = %s", (account,))

        # 獲取結果
        row = cursor.fetchone()

        # 關閉游標
        cursor.close()

        conn.close()  # 确保在使用完后关闭连接

        return row  # 返回找到的行
    except Exception as e:
        print(f"獲取資料時發生錯誤：{e}")
        return None

async def fetch_data(table_name, col, data):
    try:
        conn = create_connection()  # 每次调用时创建新的连接

        # 創建游標
        cursor = conn.cursor()

        # 執行查詢
        cursor.execute(f"SELECT * FROM {table_name} WHERE {col} = %s", (data,))

        # 獲取結果
        row = cursor.fetchone()

        # 關閉游標
        cursor.close()

        conn.close()  # 确保在使用完后关闭连接

        return row
    except Exception as e:
        print(f"Error fetching row: {e}")
        return None

# 新增資料
async def insert_data(table_name, cols, data):
    try:
        conn = create_connection()  # 每次调用时创建新的连接

        # 創建游標
        cursor = conn.cursor()

        cols_escaped = [f"`{col}`" for col in cols]
        # 建立 SQL 插入語句
        sql = f"INSERT INTO {table_name} ({','.join(cols_escaped)}) VALUES ({','.join(['%s'] * len(data))})"

        # 執行新增
        cursor.execute(sql, data)

        # 提交事務
        conn.commit()

        # 關閉游標
        cursor.close()

        conn.close()  # 确保在使用完后关闭连接

        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")

# 更新資料
async def update_data(table_name, update_info, condition_col, condition_val):
    try:
        conn = create_connection()  # 每次调用时创建新的连接

        # 創建游標
        cursor = conn.cursor()

        # 建立 SQL 更新語句的 SET 子句
        set_clause = ", ".join([f"`{key}` = '{value}'" for key, value in update_info.items()])

        # 建立 SQL 更新語句
        sql = f"UPDATE `{table_name}` SET {set_clause} WHERE `{condition_col}` = '{condition_val}'"

        # 執行更新
        cursor.execute(sql)

        # 提交事務
        conn.commit()

        # 關閉游標
        cursor.close()

        conn.close()  # 确保在使用完后关闭连接

        print("Data updated successfully.")
    except Exception as e:
        print(f"Error updating data: {e}")

#定義模型
class BaseUserModel(BaseModel):
    account: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    gender: Optional[str] = None
    verification_code: Optional[str] = None

# 創建路由
user_router = APIRouter(prefix="/USER", tags=['USER'])

# 註冊頁面
# 1.把資料填好後，按下註冊按鈕，會先去判斷帳號是否存在
# 1-1.若帳號存在，會顯示"該帳號已存在，請選擇其他帳號"
# 1-2.若帳號不存在，會執行新增資料的動作，並顯示"帳號已成功註冊"
@user_router.post("/register", summary="使用者註冊帳號")
async def register_user_account(register_data: BaseUserModel):
    try:
        # 檢查帳號是否已存在
        account_exists = await user.fetch_data("user_account", "account", register_data.account)
        if account_exists:
            return {"message": "該帳號已存在，請選擇其他帳號"}

        # 執行帳號註冊
        await user.insert_data("user_account", ["account", "email", "password", "gender"], (
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
@user_router.post("/login", summary="使用者登入帳號")
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
@user_router.post("/forgot-password", summary="忘記密碼")
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

@user_router.post("/Verify-verification_code", summary="驗證驗證碼")
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

@user_router.post("/reset-password", summary="重設密碼")
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

@user_router.get("/data", summary="獲取指定使用者的資訊")
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

@user_router.patch("/update-info", summary="修改個人資訊")
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
        await user.update_data("user_account", updated_info, "account", user_account_decoded)

        return {"message": f"{updated_info}個人資訊已成功更新", "updated_info": updated_info}
    
    except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"資料庫錯誤: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新個人資訊失敗: {str(e)}")