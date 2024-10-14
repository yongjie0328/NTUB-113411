import yfinance as yf
import pandas as pd
from prophet import Prophet

# 下載台積電的股價數據 (台積電代碼: 2330.TW)
tsmc = yf.Ticker("2330.TW")
tsmc_data = tsmc.history(start="2022-01-01", end="2024-01-01")

# 下載標普500指數數據 (代碼: ^GSPC)
sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(start="2022-01-01", end="2024-01-01")

# 檢查是否存在數據
if not tsmc_data.empty and not sp500_data.empty:
    # 添加台積電的移動平均線 (MA) 和交易量指標
    tsmc_data['MA_20'] = tsmc_data['Close'].rolling(window=20).mean()  # 20日移動平均線
    tsmc_data['Volume'] = tsmc_data['Volume']  # 保留交易量

    # 整合標普500指數數據，使用其收盤價作為外生變量
    sp500_data = sp500_data[['Close']].rename(columns={'Close': 'SP500_Close'})
    sp500_data['SP500_MA_20'] = sp500_data['SP500_Close'].rolling(window=20).mean()  # 20日移動平均線

    # 合併台積電和標普500的數據
    df = tsmc_data.reset_index().merge(sp500_data.reset_index(), on='Date', how='left')
    df['Date'] = df['Date'].dt.tz_localize(None)  # 去除時區信息
    df.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)  # Prophet 要求的列名稱

    # 準備 Prophet 模型所需的數據格式
    df['MA_20'] = df['MA_20'].fillna(method='bfill')  # 填充移動平均線的 NaN 值
    df['Volume'] = df['Volume'].fillna(method='bfill')  # 填充 NaN 值
    df['SP500_Close'] = df['SP500_Close'].fillna(method='bfill')  # 填充標普500收盤價的 NaN 值
    df['SP500_MA_20'] = df['SP500_MA_20'].fillna(method='bfill')  # 填充標普500 MA 的 NaN 值

    # 建立 Prophet 模型
    model = Prophet(daily_seasonality=True)

    # 添加外生變量
    model.add_regressor('MA_20')
    model.add_regressor('Volume')
    model.add_regressor('SP500_Close')
    model.add_regressor('SP500_MA_20')

    # 訓練 Prophet 模型
    model.fit(df)

    # 建立未來 180 天的日期
    future = model.make_future_dataframe(periods=180)

    # 添加未來數據的外生變量
    future['MA_20'] = tsmc_data['MA_20'].iloc[-1]  # 假設未來保持最近的 MA_20 水平
    future['Volume'] = tsmc_data['Volume'].iloc[-1]  # 假設未來保持最近的交易量水平
    future['SP500_Close'] = sp500_data['SP500_Close'].iloc[-1]  # 假設未來保持最近的標普500收盤價
    future['SP500_MA_20'] = sp500_data['SP500_MA_20'].iloc[-1]  # 假設未來保持最近的標普500 MA_20

    # 預測未來的股票價格
    forecast = model.predict(future)

    # 只顯示未來 180 天的預測結果
    forecast_filtered = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(180)

    # 顯示預測結果
    print(forecast_filtered)

    # 保存數據到 CSV 文件
    forecast_filtered.to_csv(r'C:\Users\jenny\Downloads\stock_forecast_with_sp500.csv', index=False)
    print("預測結果已保存到 'C:\\Users\\jenny\\Downloads\\stock_forecast_with_sp500.csv'")
else:
    print("數據未下載成功，請檢查網絡連接或日期範圍。")
