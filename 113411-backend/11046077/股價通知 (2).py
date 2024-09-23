import yfinance as yf
import requests
from time import sleep

# 設定 LINE Notify 權杖
line_notify_token = 'NRH7fHuLWTHHYtZZiBVrsiifGZasljHQpjOseKDzKQi'  # 替換為你的 LINE Notify 權杖
line_notify_api = 'https://notify-api.line.me/api/notify'

# 定義發送 LINE Notify 通知的函式
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

# 定義檢查股價的函式
def check_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')
    current_price = data['Close'].iloc[-1]  # 使用 iloc 來取得當天收盤價
    return current_price

# 主程式
if __name__ == "__main__":
    # 使用者輸入股票代碼和目標價格
    ticker = input("請輸入股票代碼: ").upper()
    target_price = float(input(f"請輸入您希望通知的目標價格 ({ticker}): "))

    print(f"開始追蹤 {ticker}，當價格達到 {target_price} 時會發送通知。")

    # 定期檢查股價
    while True:
        price = check_stock_price(ticker)
        print(f'{ticker} 的當前價格為 {price}，目標價格為 {target_price}')
        
        if price >= target_price:
            send_line_notification(ticker, price, target_price)
            break  # 通知發送後退出程式
        else:
            print(f'{ticker} 的價格尚未達到目標價格。')
        sleep(60)  # 每分鐘檢查一次
