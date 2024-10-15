from fastapi.responses import StreamingResponse
from fastapi import HTTPException, APIRouter
from .machine_learning import Stocker
import matplotlib.pyplot as plt
from datetime import datetime
import pandas_ta as ta
import yfinance as yf
import pandas as pd
import numpy as np
import io

# 創建路由
predict_router = APIRouter(prefix="/PREDICT", tags=['PREDICT'])

# 全局股票列表
stock_list = {
    '2888.TW': '新光金控',
    '2891.TW': '中信金控',
    '2883.TW': '開發金控',
    '2882.TW': '國泰金控',
    '2867.TW': '三商壽',
    '2884.TW': '玉山金控',
    '2880.TW': '華南金控',
    '2890.TW': '永豐金控',
    '2834.TW': '臺企銀',
    '2885.TW': '元大金控',
    '2303.TW': '聯電',
    '2363.TW': '矽統',
    '2330.TW': '台積電',
    '6770.TW': '力積電',
    '2344.TW': '華邦電',
    '2449.TW': '京元電子',
    '4967.TW': '十銓科技',
    '2408.TW': '南亞科',
    '3450.TW': '聯鈞',
    '3711.TW': '日月光投控',
    '2618.TW': '長榮航',
    '2609.TW': '陽明海運',
    '2610.TW': '華航',
    '2603.TW': '長榮海運',
    '2615.TW': '萬海航運',
    '2605.TW': '新興航運',
    '2634.TW': '漢翔',
    '2606.TW': '裕民航運',
    '5608.TW': '四維航運',
    '2637.TW': '慧洋海運',
    '3231.TW': '緯創',
    '2353.TW': '宏碁',
    '2382.TW': '廣達電腦',
    '2356.TW': '英業達',
    '3013.TW': '晟銘電',
    '2324.TW': '仁寶電腦',
    '2301.TW': '光寶科技',
    '2365.TW': '昆盈',
    '3017.TW': '奇鋐',
    '3706.TW': '神達',
    '2323.TW': '中環',
    '2349.TW': '錸德',
    '2374.TW': '佳能',
    '2393.TW': '億光',
    '2406.TW': '國碩',
    '2409.TW': '友達光電',
    '2426.TW': '鼎元',
    '2429.TW': '銘旺科',
    '2438.TW': '翔耀',
    '2466.TW': '冠西電'
}

# 創建股票預測功能
def create_stock_prediction(ticker: str, days: int = 90):
    df = yf.Ticker(ticker).history(period="max")
    price = df['Close']
    df.index = pd.to_datetime(df.index).tz_localize(None)

    stock = Stocker(price)
    model, model_data = stock.create_prophet_model(days=days)

    today = pd.to_datetime(datetime.now().date())
    predictions_next_30_days = model_data[model_data['ds'] >= today].head(30)

    return predictions_next_30_days[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# 過濾非交易日
def filter_non_trading_days(predictions: pd.DataFrame):
    predictions['ds'] = pd.to_datetime(predictions['ds'])
    trading_days = predictions[predictions['ds'].dt.weekday < 5]

    holidays = pd.to_datetime([
        '2024-10-05',  
        '2024-10-06',  
        '2024-10-10',  
        '2024-10-12',  
        '2024-10-13',  
        '2024-10-19',  
        '2024-10-20',  
        '2024-10-26',  
        '2024-10-27',  
        '2024-11-02',  
        '2024-11-03',  
        '2024-11-09',  
        '2024-11-10',  
        '2024-11-16',  
        '2024-11-17',  
        '2024-11-23',  
        '2024-11-24',  
        '2024-11-30',  
        '2024-12-01',  
        '2024-12-07',  
        '2024-12-08',  
        '2024-12-14',  
        '2024-12-15',  
        '2024-12-21',  
        '2024-12-22',  
        '2024-12-28',  
        '2024-12-29',  
        
    ])

    trading_days = trading_days[~trading_days['ds'].isin(holidays)]

    return trading_days

def calculate_var(returns, confidence_level=0.95):
    if len(returns) == 0:
        return None
    sorted_returns = sorted(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    return sorted_returns[index]

# 獲取股票列表
@predict_router.get("/stock-list", summary="獲取股票列表")
async def get_stock_list():
    return stock_list

# 獲取股票預測
@predict_router.get("/predict", summary="獲取股票預測")
async def predict_stock(ticker: str = '2330.TW', days: int = 90):
    if ticker not in stock_list:
        raise HTTPException(status_code=400, detail="Stock not found in the provided list.")

    try:
        predictions_df = create_stock_prediction(ticker, days)
        filtered_predictions = filter_non_trading_days(predictions_df)
        result = filtered_predictions[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records')
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 獲取當前股價
@predict_router.get("/current-price", summary="獲取當前股價")
async def current_price(ticker: str = '2330.TW'):
    if ticker not in stock_list:
        raise HTTPException(status_code=400, detail="Stock not found in the provided list.")

    try:
        df = yf.Ticker(ticker).history(period="1d")
        if df.empty:
            df = yf.Ticker(ticker).history(period="5d")
        if df.empty:
            raise HTTPException(status_code=404, detail=f'No price data found for {ticker}.')

        current_price = df['Close'].iloc[-1]
        return {"currentPrice": current_price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 生成股票預測圖像
@predict_router.get("/predict-image", summary="生成股票預測圖像")
async def predict_image(ticker: str = '2330.TW', days: int = 90):
    if ticker not in stock_list:
        raise HTTPException(status_code=400, detail="Stock not found in the provided list.")

    try:
        df = yf.Ticker(ticker).history(period="max")
        price = df['Close']
        df.index = pd.to_datetime(df.index).tz_localize(None)

        stock = Stocker(price)
        model, model_data = stock.create_prophet_model(days=days)

        today = pd.to_datetime(datetime.now().date())
        start_of_year = pd.to_datetime(datetime(today.year, 1, 1))

        actual_stock_this_year = df[df.index >= start_of_year]
        predicted_stock_this_year = model_data[model_data['ds'] >= start_of_year]

        plt.figure(figsize=(10, 6))
        plt.plot(actual_stock_this_year.index, actual_stock_this_year['Close'], label='Actual Price', color='black')
        plt.plot(predicted_stock_this_year['ds'], predicted_stock_this_year['yhat'], label='Predicted Price', color='blue')
        plt.fill_between(predicted_stock_this_year['ds'], predicted_stock_this_year['yhat_lower'], predicted_stock_this_year['yhat_upper'], color='lightblue', alpha=0.5, label='Confidence Interval')
        plt.xlabel('Date')
        plt.ylabel('Price $')
        plt.title(f'{ticker} Stock Price Prediction (This Year)')
        plt.legend()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return StreamingResponse(img, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))