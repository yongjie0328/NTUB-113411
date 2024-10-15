from fastapi import Query, HTTPException, BackgroundTasks, APIRouter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from time import sleep
import yfinance as yf
import requests
import smtplib

# 創建路由
notify_router = APIRouter(prefix="/NOTIFY", tags=['NOTIFY'])

# 股票清單
stocks = {
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

# 設置電子郵件服務器資訊
sender_email = "test113411@gmail.com"  # 你的電子郵件地址
password = "nhml qqup yswr sssm"  # 你的郵件密碼

# 發送 LINE Notify 通知的函式
def send_line_notification(ticker, price, target_price, line_notify_token):
    headers = {
        'Authorization': f'Bearer {line_notify_token}'
    }
    message = f'股票 {ticker} 的當前價格為 {price:.2f}，已達到或超過您設定的目標價格 {target_price:.2f}。'
    payload = {'message': message}
    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload)
    
    if response.status_code == 200:
        print('LINE 通知已發送')
    else:
        print(f'通知發送失敗: {response.status_code}, {response.text}')

# 發送電子郵件通知的函式
def send_email_notification(to_email, ticker, price, target_price):
    subject = f'股票 {ticker} 價格通知'
    body = f'股票 {ticker} 的當前價格為 {price:.2f}，已達到或超過您設定的目標價格 {target_price:.2f}。'

    msg = MIMEMultipart()
    msg['From'] = formataddr(("", sender_email))
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password) 
            server.send_message(msg)
        print('電子郵件通知已發送')
    except Exception as e:
        print(f'發送電子郵件失敗: {e}')

# 檢查股價的函式
def check_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            return data['Close'].iloc[-1]
        else:
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
def track_stock_price(ticker, target_price, notify_method, line_notify_token=None, email=None):
    while True:
        price = check_stock_price(ticker)
        if price is not None:
            print(f'{ticker} 的當前價格為 {price:.2f}，目標價格為 {target_price:.2f}')
            if price >= target_price:
                if notify_method == 'line' and line_notify_token:
                    send_line_notification(ticker, price, target_price, line_notify_token)
                elif notify_method == 'email' and email:
                    send_email_notification(email, ticker, price, target_price)
                break
        else:
            print(f'檢查 {ticker} 價格失敗，將在下一次檢查中重試。')
        
        sleep(60)  # 每分鐘檢查一次

@notify_router.get('/track', summary="股票價格追蹤")
def track_stock(
    ticker: str = Query(...), 
    target_price: float = Query(...), 
    notify_method: str = Query('line'),  # 預設為 LINE 通知
    line_notify_token: str = Query(None),  # 從請求中獲取 LINE Notify Token
    email: str = Query(None),  # 只有在選擇 email 通知時使用
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    if not ticker:
        raise HTTPException(status_code=400, detail="請提供股票代碼。")

    if not ticker.endswith('.TW'):
        ticker += '.TW'

    if target_price <= 0:
        raise HTTPException(status_code=400, detail="目標價格必須大於零")

    target_price = float(target_price)

    # 啟動一個獨立的執行緒來追蹤股價
    background_tasks.add_task(track_stock_price, ticker, target_price, notify_method, line_notify_token, email)

    print(f'Ticker: {ticker}, Target Price: {target_price}, Notify Method: {notify_method}')
    return {"message": f'開始追蹤 {ticker} 的股價，當達到 {target_price:.2f} 時將通知您。'}

# 獲取股票資料的 API 路由
@notify_router.get('/get_stocks', summary="股票排行")
def get_stocks():
    stock_data = []

    # 使用 yfinance 抓取資料
    for symbol, name in stocks.items():
        try:
            stock_info = yf.Ticker(symbol)
            hist = stock_info.history(period='5d') # 抓取最近五天的數據來計算漲跌幅
            eps = stock_info.info.get('trailingEps', None) # 獲取 EPS

            if not hist.empty and len(hist['Close']) > 1:
                previous_close = hist['Close'].iloc[0]
                current_close = hist['Close'].iloc[-1]

                # 計算漲跌幅
                change_percentage = ((current_close - previous_close) / previous_close * 100)
            else:
                previous_close = None
                current_close = None
                change_percentage = 0

            # 模擬三大法人交易量，這部分需要真實數據的 API
            institutional_trading_volume = stock_info.info.get('volume', 0) # 使用交易量作為示範

            stock_data.append({
                'symbol': symbol,
                'name': name,
                'tradingVolume': int(hist['Volume'].iloc[-1]) if not hist.empty else 0,
                'stockPrice': float(current_close) if current_close is not None else 0.0,
                'eps': eps if eps is not None else "N/A",
                'changePercentage': change_percentage,
                'institutionalVolume': institutional_trading_volume,
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    return stock_data