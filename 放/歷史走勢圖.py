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

# 輸入股票代碼（例如 TSM 為台積電）
ticker = 'TSM'

# 獲取股票的歷史資料
stock_data = yf.download(ticker, start='2024-06-01', end='2024-06-30')

# 繪製收盤價的歷史走勢圖
plt.figure(figsize=(10, 6))
plt.plot(stock_data['Close'], label='收盤價')
plt.title(f'{ticker} 台積電歷史走勢圖')
plt.xlabel('日期')
plt.ylabel('價格')
plt.legend()
plt.grid(True)
plt.show()
