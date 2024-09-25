from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
import yfinance as yf
from stocker import Stocker
from datetime import datetime
import io
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

# 預測函數
def create_stock_prediction(ticker, days=90):
    df = yf.Ticker(ticker).history(period="max")
    price = df['Close']
    df.index = pd.to_datetime(df.index).tz_localize(None)

    tsmc = Stocker(price)
    model, model_data = tsmc.create_prophet_model(days=days)

    today = pd.to_datetime(datetime.now().date())
    predictions_next_30_days = model_data[model_data['ds'] >= today].head(30)

    return predictions_next_30_days[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records')

# API 路由
@app.route('/predict', methods=['GET'])
def predict_stock():
    ticker = request.args.get('ticker', '2330.TW')
    days = int(request.args.get('days', 90))
    try:
        prediction = create_stock_prediction(ticker, days)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/current-price', methods=['GET'])
def current_price():
    ticker = request.args.get('ticker', '2330.TW')
    try:
        df = yf.Ticker(ticker).history(period="1d")
        current_price = df['Close'].iloc[-1]  # 獲取最近的收盤價格
        return jsonify({'currentPrice': current_price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 生成並返回預測圖像的路由
@app.route('/predict-image', methods=['GET'])
def predict_image():
    ticker = request.args.get('ticker', '2330.TW')
    days = int(request.args.get('days', 90))
    
    # 獲取股票數據
    df = yf.Ticker(ticker).history(period="max")
    price = df['Close']
    df.index = pd.to_datetime(df.index).tz_localize(None)

    # 創建 Stocker 實例
    tsmc = Stocker(price)
    model, model_data = tsmc.create_prophet_model(days=days)

    # 取得今年的數據
    today = pd.to_datetime(datetime.now().date())
    start_of_year = pd.to_datetime(datetime(today.year, 1, 1))

    # 篩選今年的實際股價和預測價格
    actual_stock_this_year = df[df.index >= start_of_year]
    predicted_stock_this_year = model_data[model_data['ds'] >= start_of_year]

    # 繪製預測圖表，並加入實際股價
    plt.figure(figsize=(10, 6))

    # 繪製實際股價
    plt.plot(actual_stock_this_year.index, actual_stock_this_year['Close'], label='Actual Price', color='black')

    # 繪製預測價格
    plt.plot(predicted_stock_this_year['ds'], predicted_stock_this_year['yhat'], label='Predicted Price', color='blue')

    # 繪製置信區間
    plt.fill_between(predicted_stock_this_year['ds'], predicted_stock_this_year['yhat_lower'], predicted_stock_this_year['yhat_upper'], color='lightblue', alpha=0.5, label='Confidence Interval')

    plt.xlabel('Date')
    plt.ylabel('Price $')
    plt.title(f'{ticker} Stock Price Prediction (This Year)')
    plt.legend()

    # 將圖像保存到二進制流中
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
