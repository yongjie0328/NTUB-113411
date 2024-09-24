import pandas as pd
import numpy as np
import yfinance as yf

# 設定股票代碼
stocks = ['2330.TW', '2317.TW']  # 台積電和鴻海
start_date = '2023-01-01'
end_date = '2024-09-20'

# 獲取股價數據
data = yf.download(stocks, start=start_date, end=end_date)['Adj Close']

# 計算每日報酬率
returns = data.pct_change().dropna()

# 計算投資組合的權重
weights = np.array([0.8, 0.2])  # 假設台積電佔60%，鴻海佔40%

# 計算投資組合的每日報酬率
portfolio_returns = returns.dot(weights)

# 計算VaR（95%信心水準）
var_95 = np.percentile(portfolio_returns, 5)

print(f"投資組合的 95% VaR: {var_95:.2%}")