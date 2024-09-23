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

# 計算短期 EMA（12天）
data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()

# 計算長期 EMA（26天）
data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()

# 計算 MACD 線
data['MACD'] = data['EMA12'] - data['EMA26']

# 計算信號線（9天的 MACD 線的 EMA）
data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

# 計算 MACD 柱狀圖
data['Histogram'] = data['MACD'] - data['Signal']

# 找到 MACD 和信號線的交叉點
cross_up = []  # 金叉
cross_down = []  # 死叉

for i in range(1, len(data)):
    if data['MACD'].iat[i-1] < data['Signal'].iat[i-1] and data['MACD'].iat[i] > data['Signal'].iat[i]:
        cross_up.append((data.index[i], data['MACD'].iat[i]))  # 記錄金叉
    elif data['MACD'].iat[i-1] > data['Signal'].iat[i-1] and data['MACD'].iat[i] < data['Signal'].iat[i]:
        cross_down.append((data.index[i], data['MACD'].iat[i]))  # 記錄死叉

# 繪製 MACD 線、信號線和柱狀圖
plt.figure(figsize=(12,6))

# 繪製 MACD 線（快線改為橙色）
plt.plot(data.index, data['MACD'], label='MACD', color='orange')

# 繪製信號線（慢線改為紫色）
plt.plot(data.index, data['Signal'], label='Signal', color='purple')

# 繪製 MACD 柱狀圖，根據條件使用不同顏色
histogram_positive = data['Histogram'][data['Histogram'] >= 0]
histogram_negative = data['Histogram'][data['Histogram'] < 0]

plt.bar(histogram_positive.index, histogram_positive, color='red', label='Positive Histogram', alpha=0.5)
plt.bar(histogram_negative.index, histogram_negative, color='green', label='Negative Histogram', alpha=0.5)

# 標記金叉和死叉點
cross_up = pd.DataFrame(cross_up, columns=['Date', 'MACD'])
cross_down = pd.DataFrame(cross_down, columns=['Date', 'MACD'])

plt.scatter(cross_up['Date'], cross_up['MACD'], color='red', marker='^', s=100, label='金叉 (MACD 上穿 Signal)')
plt.scatter(cross_down['Date'], cross_down['MACD'], color='green', marker='v', s=100, label='死叉 (MACD 下穿 Signal)')

# 添加標題和圖例
plt.title('台積電 2024 年 1 月到 6 月的 MACD 指標圖')
plt.xlabel('日期')
plt.ylabel('數值')
plt.legend()
plt.grid(True)

# 顯示圖表
plt.show()
