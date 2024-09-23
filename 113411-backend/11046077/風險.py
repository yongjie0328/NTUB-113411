import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Step 1: 下載股票數據
# 以AAPL為例，可以改為其他股票代號
ticker = 'AAPL'
data = yf.download(ticker, start='2020-01-01', end='2024-01-01')
data['returns'] = data['Adj Close'].pct_change()  # 計算日回報

# Step 2: 計算波動率
def calculate_volatility(data):
    volatility = data['returns'].std() * np.sqrt(252)  # 年化波動率
    print(f'年化波動率: {volatility:.2%}')
    return volatility

# Step 3: 計算最大回撤
def calculate_max_drawdown(data):
    # 計算累計回報
    data['cumulative_return'] = (1 + data['returns']).cumprod()
    # 計算當前到達的峰值
    data['peak'] = data['cumulative_return'].cummax()
    # 計算回撤
    data['drawdown'] = (data['cumulative_return'] - data['peak']) / data['peak']
    # 計算最大回撤
    max_drawdown = data['drawdown'].min()
    print(f'最大回撤: {max_drawdown:.2%}')
    return max_drawdown

# Step 4: 計算在險價值 (VaR)
def calculate_var(data, confidence_level=0.05):
    var = np.percentile(data['returns'].dropna(), confidence_level * 100)
    print(f'在險價值 (95%置信): {var:.2%}')
    return var

# Step 5: 視覺化風險報告
def plot_drawdown(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['cumulative_return'], label='Cumulative Return')
    plt.plot(data['peak'], label='Peak', linestyle='--')
    plt.fill_between(data.index, data['cumulative_return'], data['peak'], color='red', alpha=0.3, label='Drawdown')
    plt.legend()
    plt.title('Cumulative Return and Drawdown')
    plt.show()

# Step 6: 風險預警系統
def risk_warning(max_drawdown, threshold=-0.1):
    if max_drawdown < threshold:
        print(f'警報：最大回撤超過 {threshold*100}%！當前最大回撤為 {max_drawdown:.2%}')
    else:
        print('風險在可控範圍內。')

# Step 7: 執行所有步驟
volatility = calculate_volatility(data)
max_drawdown = calculate_max_drawdown(data)
var = calculate_var(data)
plot_drawdown(data)
risk_warning(max_drawdown, threshold=-0.1)
