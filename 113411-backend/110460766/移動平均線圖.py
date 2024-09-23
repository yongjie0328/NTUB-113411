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

# 下載台積電股票數據 (台積電代碼: 2330.TW)
tsmc = yf.Ticker("2330.TW")

# 抓取2023年的股價數據
data = tsmc.history(start="2023-01-01", end="2023-12-31")

# 計算30日移動平均線
data['30_MA'] = data['Close'].rolling(window=30).mean()

# 去除 NaN 值
data.dropna(inplace=True)

# 繪製股價和30日移動平均線圖表
plt.figure(figsize=(12,6))
plt.plot(data.index, data['Close'], label='收盤價', color='blue')
plt.plot(data.index, data['30_MA'], label='30日移動平均線', color='red')
plt.title('台積電 2024年股價與 30 日移動平均線', fontproperties=font_prop)
plt.xlabel('日期', fontproperties=font_prop)
plt.ylabel('價格 (台幣)', fontproperties=font_prop)
plt.legend(prop=font_prop)
plt.grid(True)
plt.show()
