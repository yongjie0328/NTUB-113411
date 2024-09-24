import numpy as np
import pandas as pd
import yfinance as yf

# 設定股票代碼和時間範圍
stock_symbol = '2330.TW'  # 台積電
start_date = '2021-01-01'
end_date = '2023-12-31'

# 下載台積電的歷史價格數據
data = yf.download(stock_symbol, start=start_date, end=end_date)

# 確保數據是否正常下載
if data.empty:
    print("股票數據下載失敗，請檢查網絡連接或股票代碼。")
else:
    # 計算每日的報酬率
    data['Returns'] = data['Adj Close'].pct_change().dropna()

    # 剔除報酬率為 0 的數據，並剔除極端值
    data = data[(data['Returns'] != 0) & (data['Returns'].abs() > 0.0001)]

    # 檢查報酬率數據的基本統計信息
    print("剔除極端值後的報酬率基本統計信息：")
    print(data['Returns'].describe())

    # 確保報酬率數據不為空
    if data['Returns'].empty:
        print("有效的報酬率數據為空，無法計算 VaR")
    else:
        # 設定信心水準
        confidence_level = 0.95  # 95% 信心水準

        # 使用歷史模擬法計算 VaR
        var_percentile = (1 - confidence_level) * 100
        VaR = np.percentile(data['Returns'], var_percentile)

        # 顯示結果
        print(f"台積電的 95% 信心水準 VaR: {VaR:.2%}")

        # 打印最近的數據樣本
        print("台積電的歷史數據:")
        print(data.tail(10))

