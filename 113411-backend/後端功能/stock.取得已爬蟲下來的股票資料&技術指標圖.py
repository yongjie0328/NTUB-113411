from fastapi import Query, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fastapi import APIRouter
import mysql.connector
import pandas as pd
import os

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


# 製作技術分析指標圖表
# 讀取 CSV 檔案
csv_filename = 'stock_technical_analysis/sii_stock_technical_analysis.csv'
df = pd.read_csv(csv_filename)

# 確保目標資料夾存在
output_dir = './stock_technical_analysis/stock_technical_analysis_image/'
os.makedirs(output_dir, exist_ok=True)  # 如果資料夾不存在則創建

# 轉換日期格式
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')  # 根據您的日期格式進行調整

# 獲取所有唯一的股票代碼
tickers = df['Ticker'].unique()

@stock_router.get("/generate-chart", summary="獲取股票技術分析圖表")
async def plot_stock_charts(
    ticker: str = Query(..., description="股票代碼"),
    charts: str = Query(..., description="選擇的技術指標 (可選: 成交量, MA, MACD, RSI, KD,) ")
):
    ticker_with_suffix = f"{ticker}.TW"  # 加上 .TW

    if ticker_with_suffix not in tickers:
        raise HTTPException(status_code=404, detail="未找到股票代碼")

    selected_charts = [chart.strip() for chart in charts.split(',')]
    ticker_data = df[df['Ticker'] == ticker_with_suffix]  # 用修改後的 ticker 進行篩選

    # 檢查數據是否有效
    if ticker_data.empty:
        raise HTTPException(status_code=404, detail="沒有找到指定股票代碼的數據")

    # 創建子圖
    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]], subplot_titles=[f"{ticker_with_suffix} 指標圖"])

    # 繪製用戶選擇的圖表到子圖中
    if '成交量' in selected_charts:
        print("新增成交量圖表")
        fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], name='成交量', marker_color='lightblue'), secondary_y=False)

    if 'MA' in selected_charts:
        print("新增移動平均線圖表")
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='收盤價', line=dict(color='blue')), secondary_y=False)
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['MA20'], mode='lines', name='MA20', line=dict(color='orange')), secondary_y=False)
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['MA50'], mode='lines', name='MA50', line=dict(color='green')), secondary_y=False)

    if 'MACD' in selected_charts:
        print("新增 MACD 圖表")
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['MACD'], mode='lines', name='MACD', line=dict(color='purple')), secondary_y=True)
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Signal Line'], mode='lines', name='信號線', line=dict(color='red')), secondary_y=True)

    if 'RSI' in selected_charts:
        print("新增 RSI 圖表")
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], mode='lines', name='RSI', line=dict(color='brown')), secondary_y=False)

    if 'KD' in selected_charts:
        print("新增KD圖表")
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['K'], mode='lines', name='K 值', line=dict(color='pink')), secondary_y=True)
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['D'], mode='lines', name='D 值', line=dict(color='lightgreen')), secondary_y=True)

    # 更新布局
    fig.update_layout(title=f'{ticker_with_suffix} 技術指標圖', template='plotly_white', height=600)
    fig.update_yaxes(title_text='價格', secondary_y=False)
    fig.update_yaxes(title_text='指標', secondary_y=True)

    # 保存圖表
    chart_file = os.path.join(output_dir, f"{ticker_with_suffix}_chart.html")
    fig.write_html(chart_file)

    return HTMLResponse(content=open(chart_file).read())