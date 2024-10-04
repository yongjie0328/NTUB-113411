from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import requests
from threading import Thread
from time import sleep

app = Flask(__name__)
# 設置 CORS，允許來自前端的請求
CORS(app, resources={r"/track": {"origins": "http://192.168.50.15:8080"}})

# 設定 LINE Notify 權杖
line_notify_token = '7XEC8eQBn76FFaj9WgRm3iBWCIR4SNkRO1VNYivUwZN'  # 請替換為正確的 LINE Notify 權杖
line_notify_api = 'https://notify-api.line.me/api/notify'

# 發送 LINE Notify 通知的函式
def send_line_notification(ticker, price, target_price):
    headers = {
        'Authorization': f'Bearer {line_notify_token}'
    }
    message = f'股票 {ticker} 的當前價格為 {price:.2f}，已達到或超過您設定的目標價格 {target_price:.2f}。'
    payload = {'message': message}
    response = requests.post(line_notify_api, headers=headers, data=payload)
    
    if response.status_code == 200:
        print('LINE 通知已發送')
    else:
        print('通知發送失敗', response.status_code)

# 檢查股價的函式
def check_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            return data['Close'].iloc[-1]
        else:
            # 如果當前沒有可用數據，嘗試抓取最近五天的數據
            print(f'無法獲取 {ticker} 的當日股價，嘗試獲取最近五天的數據...')
            data = stock.history(period='5d')
            if not data.empty:
                return data['Close'].iloc[-1]
            else:
                print(f'無法獲取 {ticker} 的股價數據。')
                return None
    except Exception as e:
        print(f'檢查股價時出錯: {e}')
        return None

# 追蹤股價的函式
def track_stock_price(ticker, target_price):
    while True:
        price = check_stock_price(ticker)
        if price is not None:
            print(f'{ticker} 的當前價格為 {price:.2f}，目標價格為 {target_price:.2f}')
            if price >= target_price:
                send_line_notification(ticker, price, target_price)
                break
        else:
            print(f'檢查 {ticker} 價格失敗，將在下一次檢查中重試。')
        
        sleep(60)  # 每分鐘檢查一次

# API 路由，讓使用者提交股票代碼和目標價格
@app.route('/track', methods=['GET'])
def track_stock():
    print('Received request for tracking stock.')
    ticker = request.args.get('ticker')
    target_price = request.args.get('target_price')

    if not ticker:
        return jsonify({'message': '請提供股票代碼。'}), 400

    # 檢查 ticker 是否以 ".TW" 結尾，如果沒有則添加
    if not ticker.endswith('.TW'):
        ticker += '.TW'

    if not target_price or float(target_price) <= 0:
        return jsonify({'message': '目標價格必須大於零。'}), 400

    target_price = float(target_price)

    # 啟動一個獨立的執行緒來追蹤股價，避免阻塞主程式
    thread = Thread(target=track_stock_price, args=(ticker, target_price))
    thread.start()

    print(f'Ticker: {ticker}, Target Price: {target_price}')
    return jsonify({'message': f'開始追蹤 {ticker} 的股價，當達到 {target_price:.2f} 時將通知您。'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
