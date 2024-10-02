import yfinance as yf
import pandas as pd

# 抓取台積電的歷史數據，股票代號為 "2330.TW"
tsmc = yf.download('2330.TW', start='2020-01-01', end='2024-01-01')

# 計算 MA10 和 MA50
tsmc['MA10'] = tsmc['Close'].rolling(window=10).mean()
tsmc['MA50'] = tsmc['Close'].rolling(window=50).mean()

# 計算 Price_Ratio
tsmc['Price_Ratio'] = tsmc['Close'] / tsmc['Close'].shift(1)


# 計算 RSI 指標
def calculate_rsi(data, window=14):
    delta = data.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

tsmc['RSI'] = calculate_rsi(tsmc['Close'])

# 顯示每天的完整數據，包括計算出的技術指標
print(tsmc[['Open', 'High', 'Low', 'Close', 'Volume', 'MA10', 'MA50', 'RSI','Price_Ratio']].tail())

# 保存到 CSV 文件（可選）
tsmc[['Open', 'High', 'Low', 'Close', 'Volume', 'MA10', 'MA50', 'RSI']].to_csv('TSMC_technical_indicators_with_daily_data.csv')
