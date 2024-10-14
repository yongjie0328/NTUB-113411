from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import os

# 獲取當前日期
end_date = datetime.now()
# 計算120天前的日期
start_date = end_date - timedelta(days=120)

# 格式化日期為字串
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# 下載股票歷史數據
tickers = ['2888.TW', '2891.TW', '2883.TW', '2882.TW', '2867.TW',
           '2884.TW', '2880.TW', '2890.TW', '2834.TW', '2885.TW',
           '2303.TW', '2363.TW', '2330.TW', '6770.TW', '2344.TW',
           '2449.TW', '4967.TW', '2408.TW', '3450.TW', '3711.TW',
           '2618.TW', '2609.TW', '2610.TW', '2603.TW', '2615.TW',
           '2605.TW', '2634.TW', '2606.TW', '5608.TW', '2637.TW',
           '3231.TW', '2353.TW', '2382.TW', '2356.TW', '3013.TW',
           '2324.TW', '2301.TW', '2365.TW', '3017.TW', '3706.TW',
           '2323.TW', '2349.TW', '2374.TW', '2393.TW', '2406.TW',
           '2409.TW', '2426.TW', '2429.TW', '2438.TW', '2466.TW']

# 創建一個空的DataFrame用於存儲所有股票的技術指標
all_technical_indicators = pd.DataFrame()

# 下載過去120天的股票數據
for ticker in tickers:
    df = yf.download(ticker, start=start_date_str, end=end_date_str)

    # 計算技術指標
    df['Ticker'] = ticker  # 添加股票代碼列
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()

    # MACD
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # RSI
    delta = df['Close'].diff(1)
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # KD指標
    low_min = df['Low'].rolling(window=9).min()
    high_max = df['High'].rolling(window=9).max()
    df['RSV'] = (df['Close'] - low_min) / (high_max - low_min) * 100
    df['K'] = df['RSV'].ewm(alpha=1/3, adjust=False).mean()
    df['D'] = df['K'].ewm(alpha=1/3, adjust=False).mean()

    # 將每隻股票的技術指標添加到總的DataFrame中
    all_technical_indicators = pd.concat([all_technical_indicators, df])

# 保存所有股票的技術指標到一個CSV檔案
output_folder = 'stock_technical_analysis'  # 確保使用已存在的資料夾
all_csv_filename = os.path.join(output_folder, 'sii_stock_technical_analysis.csv')
all_technical_indicators.to_csv(all_csv_filename)
print(f'所有股票的技術指標已保存為 {all_csv_filename}')