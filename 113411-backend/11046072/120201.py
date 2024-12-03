from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from plotly.graph_objects import Figure, Scatter
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.losses import Huber
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import logging
from datetime import datetime
import math
import pandas_market_calendars as mcal

# 初始化 FastAPI 應用程式
app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設定日誌
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# 確保 static 目錄存在
os.makedirs("static", exist_ok=True)

# 定義請求資料模型
class PredictionRequest(BaseModel):
    ticker: str
    start_date: str = "2014-01-01"
    end_date: str = datetime.today().strftime('%Y-%m-%d')

class BacktestRequest(BaseModel):
    ticker: str
    investment: float
    start_date: str = "2014-01-01"
    end_date: str = datetime.today().strftime('%Y-%m-%d')

# 工具函數
def preprocess_stock_data(ticker, start_date, end_date):
    """下載並處理股票數據"""
    # 下載股票數據
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    if stock_data.empty:
        raise ValueError("無法下載股票數據，請確認股票代號是否正確。")

    # 確保今天的日期被處理，即使是非交易日
    today_date = pd.Timestamp(datetime.today().strftime('%Y-%m-%d'))
    if stock_data.index[-1] != today_date:
        # 如果最後的交易日不是今天，則添加今天的數據並使用最後交易日數據填充
        today_data = stock_data.iloc[-1].copy()
        today_data.name = today_date
        stock_data = pd.concat([stock_data, pd.DataFrame([today_data], index=[today_date])])
        logger.info(f"已添加今日數據（非交易日）：{today_data.name}")

    # 使用最近交易日數據填充非交易日
    stock_data = stock_data.asfreq('B', method='ffill')  # 'B' 是工作日頻率，'ffill' 向前填充

    # 增加技術指標
    stock_data['MA_10'] = stock_data['Close'].rolling(window=10).mean()
    stock_data['MA_50'] = stock_data['Close'].rolling(window=50).mean()
    delta = stock_data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))
    stock_data['MACD'] = stock_data['Close'].ewm(span=12, adjust=False).mean() - stock_data['Close'].ewm(span=26, adjust=False).mean()
    high_low = stock_data['High'] - stock_data['Low']
    high_close = abs(stock_data['High'] - stock_data['Close'].shift())
    low_close = abs(stock_data['Low'] - stock_data['Close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    stock_data['ATR'] = true_range.rolling(window=14).mean()
    stock_data.dropna(inplace=True)  # 移除技術指標計算後的空值

    if stock_data.empty:
        raise ValueError("計算技術指標後數據集中沒有可用數據，請檢查輸入的日期範圍或股票代號。")

    return stock_data




def build_bidirectional_lstm_model(input_shape):
    """建立雙向 LSTM 模型"""
    model = Sequential([
        Bidirectional(LSTM(128, return_sequences=True, input_shape=input_shape)),
        Dropout(0.2),
        Bidirectional(LSTM(64, return_sequences=True)),
        Dropout(0.2),
        Bidirectional(LSTM(32)),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss=Huber(delta=1.0))
    return model


def predict_next_days_with_today(model, scaled_data, look_back, future_days):
    """滾動預測未來價格，包含當日"""
    predictions = []
    input_seq = scaled_data[-look_back:]
    for step in range(future_days + 1):  # 包含當日預測
        input_seq = np.expand_dims(input_seq, axis=0)
        predicted_scaled = model.predict(input_seq, verbose=0)
        new_row = np.hstack([predicted_scaled[0], input_seq[0, -1, 1:]])
        input_seq = np.vstack([input_seq[0, 1:], new_row])
        predictions.append(predicted_scaled[0, 0])
    return predictions


@app.post("/predict/")
async def predict(data: PredictionRequest):
    try:
        ticker = data.ticker.upper()
        logger.info(f"開始處理預測請求：{ticker}")

        # 下載並處理數據
        stock_data = preprocess_stock_data(ticker, data.start_date, data.end_date)
        features = ['Close', 'MA_10', 'MA_50', 'RSI', 'MACD', 'ATR']
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(stock_data[features])

        # 構建 LSTM 模型
        look_back = 30
        X, y = [], []
        for i in range(look_back, len(scaled_data)):
            X.append(scaled_data[i - look_back:i])
            y.append(scaled_data[i, 0])
        X, y = np.array(X), np.array(y)

        model = build_bidirectional_lstm_model((X.shape[1], X.shape[2]))
        reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, min_lr=1e-6)
        early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
        model.fit(X, y, epochs=100, batch_size=32, callbacks=[reduce_lr, early_stopping], verbose=1)

        # 預測當日和未來 15 天價格
        future_days = 15
        all_scaled_predictions = predict_next_days_with_today(model, scaled_data, look_back, future_days)

        # 補齊特徵數量並反標準化價格
        all_prices_with_features = np.hstack([
            np.array(all_scaled_predictions).reshape(-1, 1),
            np.tile(scaled_data[-1, 1:], (len(all_scaled_predictions), 1))
        ])
        logger.info(f"all_prices_with_features shape: {all_prices_with_features.shape}")
        all_prices = scaler.inverse_transform(all_prices_with_features)[:, 0]

        # 修正歷史價格的反標準化
        actual_prices_with_features = np.hstack([
            scaled_data[:, :1],  # 僅價格列
            np.tile(scaled_data[-1, 1:], (len(scaled_data), 1))  # 補全其他特徵
        ])
        actual_prices = scaler.inverse_transform(actual_prices_with_features)[:, 0]

        # 當日預測
        today_prediction = all_prices[0]

        # 未來 15 天預測
        future_prices = all_prices[1:]

        # 生成互動圖表
        future_dates = pd.date_range(start=stock_data.index[-1], periods=future_days + 1)[1:]
        fig = Figure()

        # 添加實際價格
        fig.add_trace(Scatter(
            x=stock_data.index[-len(y):],
            y=actual_prices[-len(y):],
            mode='lines',
            name='Actual Prices',
            line=dict(color='black')
        ))

        # 添加當日價格
        fig.add_trace(Scatter(
            x=[stock_data.index[-1]],
            y=[today_prediction],
            mode='markers',
            name='Today Prediction',
            marker=dict(color='blue', size=10)
        ))

        # 添加未來預測價格
        fig.add_trace(Scatter(
            x=future_dates,
            y=future_prices,
            mode='lines+markers',
            name='Future Predictions',
            line=dict(color='orange', dash='dot')
        ))

        # 設置圖表佈局
        fig.update_layout(
            title=f"Prediction with Future 15-Day Forecast for {ticker}",
            xaxis_title="Date",
            yaxis_title="Price",
            legend=dict(x=0, y=1),
            template="plotly_white"
        )

        # 保存為 HTML 文件
        pred_chart_path = f"static/prediction_with_future_{ticker}.html"
        fig.write_html(pred_chart_path)
        logger.info(f"圖表已保存至: {pred_chart_path}")

        return {
            "prediction_chart_path": f"/static/prediction_with_future_{ticker}.html",
            "actual_prices": actual_prices.tolist(),
            "actual_prices_dates": stock_data.index.strftime('%Y-%m-%d').tolist(),  # 實際日期
            "today_prediction": today_prediction,
            "future_prices": future_prices.tolist(),
            "future_prices_dates": future_dates.strftime('%Y-%m-%d').tolist(),  # 未來日期
        }

    except Exception as e:
        logger.error(f"預測失敗：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/backtest/")
async def backtest(data: BacktestRequest):
    try:
        ticker = data.ticker.upper()
        logger.info(f"開始處理回測請求：{ticker}")

        # 下載並處理數據
        stock_data = preprocess_stock_data(ticker, data.start_date, data.end_date)
        features = ['Close', 'MA_10', 'MA_50', 'RSI', 'MACD', 'ATR']
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(stock_data[features])

        # 構建 LSTM 模型
        look_back = 30
        X, y = [], []
        for i in range(look_back, len(scaled_data)):
            X.append(scaled_data[i - look_back:i])
            y.append(scaled_data[i, 0])
        X, y = np.array(X), np.array(y)

        model = build_bidirectional_lstm_model((X.shape[1], X.shape[2]))
        reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, min_lr=1e-6)
        early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
        model.fit(X, y, epochs=100, batch_size=32, callbacks=[reduce_lr, early_stopping], verbose=1)

        # 使用模型進行回測
        predictions = model.predict(X, verbose=0).flatten()
        predicted_prices = scaler.inverse_transform(
            np.hstack([predictions.reshape(-1, 1), scaled_data[:len(predictions), 1:]])
        )[:, 0]

        actual_prices = scaler.inverse_transform(
            np.hstack([scaled_data[:len(predictions), 0].reshape(-1, 1), scaled_data[:len(predictions), 1:]])
        )[:, 0]

        # 投資回測邏輯
        portfolio_value = [data.investment]
        cash = data.investment
        holdings = 0
        buy_signals = []
        sell_signals = []

        for i in range(len(predicted_prices)):
            if i == 0:
                continue

            if predicted_prices[i] > predicted_prices[i - 1] and cash > 0:  # 買入
                holdings = cash / actual_prices[i]
                cash = 0
                buy_signals.append((i, actual_prices[i]))

            elif predicted_prices[i] < predicted_prices[i - 1] and holdings > 0:  # 賣出
                cash = holdings * actual_prices[i]
                holdings = 0
                sell_signals.append((i, actual_prices[i]))

            portfolio_value.append(cash + holdings * actual_prices[i])

        # 計算回測指標
        total_return = (portfolio_value[-1] - data.investment) / data.investment * 100
        max_drawdown = max(np.maximum.accumulate(portfolio_value) - portfolio_value)
        daily_returns = np.diff(portfolio_value) / portfolio_value[:-1]
        sharpe_ratio = (
            np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252)
            if len(daily_returns) > 1 and np.std(daily_returns) > 0
            else 0
        )

        # 生成回測圖表
        backtest_chart_path = f"static/backtest_result_{ticker}.html"
        fig = Figure()
        fig.add_trace(Scatter(
            x=stock_data.index[:len(portfolio_value)],
            y=portfolio_value,
            mode='lines',
            name='Portfolio Value',
            line=dict(color='green')
        ))
        fig.add_trace(Scatter(
            x=[stock_data.index[i] for i, _ in buy_signals],
            y=[price for _, price in buy_signals],
            mode='markers',
            name='Buy Signals',
            marker=dict(color='blue', size=10)
        ))
        fig.add_trace(Scatter(
            x=[stock_data.index[i] for i, _ in sell_signals],
            y=[price for _, price in sell_signals],
            mode='markers',
            name='Sell Signals',
            marker=dict(color='red', size=10)
        ))
        fig.update_layout(
            title=f"Backtest Portfolio Performance for {ticker}",
            xaxis_title="Date",
            yaxis_title="Portfolio Value",
            legend=dict(x=0, y=1),
            template="plotly_white"
        )
        fig.write_html(backtest_chart_path)
        logger.info(f"回測圖表已保存至: {backtest_chart_path}")

        return {
            "backtest_chart_path": f"/static/backtest_result_{ticker}.html",
            "total_return": total_return,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
        }
    except Exception as e:
        logger.error(f"回測失敗：{e}")
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/static", StaticFiles(directory="static"), name="static")

