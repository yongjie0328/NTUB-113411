from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
import yfinance as yf
from stocker import Stocker
from datetime import datetime
import io
import matplotlib
import matplotlib.pyplot as plt

# Use a non-interactive backend
matplotlib.use('Agg')

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

# 股票清單
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

@app.route('/stock-list', methods=['GET'])
def get_stock_list():
    return jsonify(stock_list)

# API 路由
@app.route('/predict', methods=['GET'])
def predict_stock():
    ticker = request.args.get('ticker', '2330.TW')
    
    # 檢查股票代碼是否在列表中
    if ticker not in stock_list:
        return jsonify({'error': 'Stock not found in the provided list.'}), 400
    
    days = int(request.args.get('days', 90))
    try:
        prediction = create_stock_prediction(ticker, days)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/current-price', methods=['GET'])
def current_price():
    ticker = request.args.get('ticker', '2330.TW')
    
    # 檢查股票代碼是否在列表中
    if ticker not in stock_list:
        return jsonify({'error': 'Stock not found in the provided list.'}), 400
    
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
