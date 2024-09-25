from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import requests
from threading import Thread
from time import sleep

app = Flask(__name__)
CORS(app)  # 啟用 CORS 支援

# 設定 LINE Notify 權杖
line_notify_token = 'NRH7fHuLWTHHYtZZiBVrsiifGZasljHQpjOseKDzKQi'
line_notify_api = 'https://notify-api.line.me/api/notify'

# 發送 LINE Notify 通知的函式
def send_line_notification(ticker, price, target_price):
    headers = {
        'Authorization': f'Bearer {line_notify_token}'
    }
    message = f'股票 {ticker} 的當前價格為 {price}，已達到或超過您設定的目標價格 {target_price}。'
    payload = {'message': message}
    response = requests.post(line_notify_api, headers=headers, data=payload)
    if response.status_code == 200:
        print('LINE 通知已發送')
    else:
        print('通知發送失敗', response.status_code)

# 檢查股價的函式
def check_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')
    current_price = data['Close'].iloc[-1]
    return current_price

# 追蹤股價的函式
def track_stock_price(ticker, target_price):
    while True:
        price = check_stock_price(ticker)
        print(f'{ticker} 的當前價格為 {price}，目標價格為 {target_price}')
        if price >= target_price:
            send_line_notification(ticker, price, target_price)
            break
        sleep(60)  # 每分鐘檢查一次

# API 路由，讓使用者提交股票代碼和目標價格
@app.route('/track', methods=['GET'])
def track_stock():
    ticker = request.args.get('ticker')
    target_price = float(request.args.get('target_price'))

    # 啟動一個獨立的執行緒來追蹤股價，避免阻塞主程式
    thread = Thread(target=track_stock_price, args=(ticker, target_price))
    thread.start()

    return jsonify({'message': f'開始追蹤 {ticker} 的股價，當達到 {target_price} 時將通知您。'})

if __name__ == '__main__':
    app.run(debug=True)


