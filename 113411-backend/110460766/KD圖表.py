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

# 檢查數據是否正確下載
print(data.head())  # 確認前幾行數據是否存在

# 檢查是否存在數據
if data.empty:
    print("數據未下載成功，請檢查網絡連接或日期範圍。")
else:
    # 計算 RSV、K、D 值
    n = 9  # 通常 n 為 9 天
    data['Lowest_9'] = data['Low'].rolling(window=n).min()
    data['Highest_9'] = data['High'].rolling(window=n).max()
    
    # 檢查 RSV 計算是否正確
    data['RSV'] = (data['Close'] - data['Lowest_9']) / (data['Highest_9'] - data['Lowest_9']) * 100
    print(data[['Close', 'Lowest_9', 'Highest_9', 'RSV']].tail())  # 打印 RSV 計算結果
    
    # 初始化 K 和 D 值
    data['K'] = 50  # K 值初始為 50
    data['D'] = 50  # D 值初始為 50

    # 計算 K 和 D 值
    for i in range(1, len(data)):
        if pd.notna(data['RSV'].iat[i]):
            data['K'].iat[i] = 2/3 * data['K'].iat[i-1] + 1/3 * data['RSV'].iat[i]
            data['D'].iat[i] = 2/3 * data['D'].iat[i-1] + 1/3 * data['K'].iat[i]

    # 檢查是否計算出 K 和 D 值
    print(data[['K', 'D']].tail())  # 打印 K 和 D 的最後幾行以進行檢查

    # 去除 NaN 值
    data.dropna(inplace=True)

    # 繪製 KD 圖表
    plt.figure(figsize=(12,6))
    plt.plot(data.index, data['K'], label='K值', color='red')
    plt.plot(data.index, data['D'], label='D值', color='blue')
    plt.title('台積電 2024 年 1 月到 6 月的 KD 指標圖')
    plt.xlabel('日期')
    plt.ylabel('KD 值')
    plt.legend()
    plt.grid(True)

    # 顯示圖表
    plt.show()
