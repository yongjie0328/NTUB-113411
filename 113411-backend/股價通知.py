import yfinance as yf
import requests
from time import sleep

# 設定股票代碼和目標價格
ticker = '2330.tw'  # 股票代碼
target_price = 975.00  # 目標價格

# 設定 LINE Notify 權杖
line_notify_token = 'NRH7fHuLWTHHYtZZiBVrsiifGZasljHQpjOseKDzKQi'
line_notify_api = 'https://notify-api.line.me/api/notify'

def send_line_notification(price):
    headers = {
        'Authorization': f'Bearer {line_notify_token}'
    }
    message = f'{ticker} 的當前價格為 {price}，已達到或超過目標價格 {target_price}。'
    payload = {'message': message}
    response = requests.post(line_notify_api, headers=headers, data=payload)
    if response.status_code == 200:
        print('LINE 通知已發送')
    else:
        print('通知發送失敗', response.status_code)

def check_stock_price():
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')
    current_price = data['Close'].iloc[-1]  # 使用 iloc 來取得當天收盤價
    return current_price

# 定期檢查股價
while True:
    price = check_stock_price()
    if price >= target_price:
        send_line_notification(price)
        break
    else:
        print(f'{ticker} 的當前價格為 {price}，尚未達到目標價格 {target_price}')
    sleep(30)  # 每分鐘檢查一次
