from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route import otc_stock, sii_stock, user

app = FastAPI()

# 將路由器添加到應用程式中
app.include_router(otc_stock.router)
app.include_router(sii_stock.router)
app.include_router(user.router)

# 定義允許的來源
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://192.168.50.174:8000",
    # 要在新增前端的IP
    "http://192.168.50.19:8080",
    "http://192.168.120.30:8888"
]

# 設置 CORS 中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

