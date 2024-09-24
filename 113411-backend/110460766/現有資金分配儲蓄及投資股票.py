import numpy as np
import pandas as pd
import yfinance as yf

# 設定總資金 (單位: 新台幣)
total_funds = 100000  # 假設總資金是 100,000 元

# 設定資金分配比例
savings_ratio = 0.3  # 30% 資金存入儲蓄
investment_ratio = 0.7  # 70% 資金用於股票投資

# 計算儲蓄及投資金額
savings_amount = total_funds * savings_ratio
investment_amount = total_funds * investment_ratio

print(f"總資金: {total_funds} 元")
print(f"分配到儲蓄的金額: {savings_amount} 元")
print(f"分配到投資股票的金額: {investment_amount} 元")

# 設定股票代碼和投資比例（假設投資多個股票）
stocks = ['2330.TW', '2317.TW']  # 台積電和鴻海
stock_ratios = [0.6, 0.4]  # 假設台積電佔60%，鴻海佔40%

# 計算每個股票的投資金額
stock_investments = np.array(stock_ratios) * investment_amount

for i, stock in enumerate(stocks):
    print(f"分配到 {stock} 的金額: {stock_investments[i]:.2f} 元")

# 獲取股票價格並計算購買股數
for i, stock in enumerate(stocks):
    data = yf.Ticker(stock)
    stock_price = data.history(period='1d')['Close'][0]
    shares = stock_investments[i] // stock_price  # 計算能購買的股數
    print(f"{stock} 現價: {stock_price:.2f} 元，能購買的股數: {shares} 股")
