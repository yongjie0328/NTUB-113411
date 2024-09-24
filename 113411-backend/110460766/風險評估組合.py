import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# 1. 獲取數據：下載一組資產的歷史價格數據，例如 S&P 500 指數
data = yf.download('^GSPC', start='2020-01-01', end='2023-12-31')

# 2. 計算每日回報率
data['Returns'] = data['Adj Close'].pct_change()

# 3. 計算回報的標準差（波動性）
volatility = data['Returns'].std() * np.sqrt(252)  # 年化波動性
print(f"年化波動性: {volatility}")

# 4. 計算 VaR (假設置信水準為95%)
confidence_level = 0.05
VaR_95 = np.percentile(data['Returns'].dropna(), confidence_level * 100)
print(f"95% VaR: {VaR_95}")

# 5. 繪製每日回報率的分佈圖
plt.hist(data['Returns'].dropna(), bins=50, alpha=0.75)
plt.axvline(x=VaR_95, color='red', linestyle='--', label=f'95% VaR: {VaR_95:.4f}')
plt.title('S&P 500 Daily Returns Distribution')
plt.xlabel('Daily Returns')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()
