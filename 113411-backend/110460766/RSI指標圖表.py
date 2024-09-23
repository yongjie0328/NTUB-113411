import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import yfinance as yf
import pandas as pd

# 指定 corbelb.ttf 字體的正確路徑
font_path = r'c:\WINDOWS\Fonts\KAIU.TTF'  # 修改為你實際的字體文件路徑
font_prop = fm.FontProperties(fname=font_path)

# 使用指定的 corbelb 字體
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]  # 設置字體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題


# 下載台積電的股價數據 (台積電代碼: 2330.TW)
tsmc = yf.Ticker("2330.TW")
data = tsmc.history(start="2024-01-01", end="2024-06-30")

# 計算漲跌幅
data['Change'] = data['Close'].diff()

# 計算漲跌幅中漲幅（正值）和跌幅（負值）
data['Gain'] = data['Change'].where(data['Change'] > 0, 0)
data['Loss'] = -data['Change'].where(data['Change'] < 0, 0)

# 計算平均漲幅和平均跌幅（14 天）
n = 14
data['Avg_Gain'] = data['Gain'].rolling(window=n, min_periods=1).mean()
data['Avg_Loss'] = data['Loss'].rolling(window=n, min_periods=1).mean()

# 計算相對強度（RS）
data['RS'] = data['Avg_Gain'] / data['Avg_Loss']

# 計算 RSI 指標
data['RSI'] = 100 - (100 / (1 + data['RS']))

# 繪製 RSI 圖表
plt.figure(figsize=(12,6))

plt.plot(data.index, data['RSI'], label='RSI', color='blue')

# 繪製超買和超賣水平線
plt.axhline(y=70, color='red', linestyle='--', label='超買區 (70)')
plt.axhline(y=30, color='green', linestyle='--', label='超賣區 (30)')

# 添加標題和圖例
plt.title('台積電 2024 年 1 月到 6 月的 RSI 指標圖')
plt.xlabel('日期')
plt.ylabel('RSI 值')
plt.legend()
plt.grid(True)

# 顯示圖表
plt.show()
