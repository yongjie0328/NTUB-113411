import yfinance as yf
import pandas as pd
from prophet import Prophet

# 設置時間範圍
start_date = "2010-01-01"
end_date = "2024-01-01"

try:
    # 下載台積電的股價數據 (台積電代碼: 2330.TW)
    tsmc = yf.Ticker("2330.TW")
    tsmc_data = tsmc.history(start=start_date, end=end_date)
    
    # 檢查台積電數據是否成功下載
    if tsmc_data.empty:
        raise ValueError("無法下載台積電的數據，請檢查股票代碼和日期範圍。")

    # 下載標普500指數數據 (代碼: ^GSPC)
    sp500 = yf.Ticker("^GSPC")
    sp500_data = sp500.history(start=start_date, end=end_date)

    # 檢查標普500數據是否成功下載
    if sp500_data.empty:
        raise ValueError("無法下載標普500的數據，請檢查指數代碼和日期範圍。")

    # 合併台積電和標普500的數據，保留台積電的交易日
    df = tsmc_data.reset_index().merge(sp500_data.reset_index(), on='Date', how='left', suffixes=('_TSMC', '_SP500'))
    df['Date'] = df['Date'].dt.tz_localize(None)  # 去除時區信息
    df.rename(columns={'Date': 'ds', 'Close_TSMC': 'y'}, inplace=True)  # Prophet 要求的列名稱

    # 計算 MACD 和信號線
    df['EMA_12_TSMC'] = df['y'].ewm(span=12, adjust=False).mean()
    df['EMA_26_TSMC'] = df['y'].ewm(span=26, adjust=False).mean()
    df['MACD_TSMC'] = df['EMA_12_TSMC'] - df['EMA_26_TSMC']
    df['Signal_Line_TSMC'] = df['MACD_TSMC'].ewm(span=9, adjust=False).mean()

    df['EMA_12_SP500'] = df['Close_SP500'].ewm(span=12, adjust=False).mean()
    df['EMA_26_SP500'] = df['Close_SP500'].ewm(span=26, adjust=False).mean()
    df['MACD_SP500'] = df['EMA_12_SP500'] - df['EMA_26_SP500']
    df['Signal_Line_SP500'] = df['MACD_SP500'].ewm(span=9, adjust=False).mean()

    # 填充 NaN 值（特別是標普500的數據）
    df['MACD_TSMC'] = df['MACD_TSMC'].ffill().bfill()
    df['Signal_Line_TSMC'] = df['Signal_Line_TSMC'].ffill().bfill()
    df['MACD_SP500'] = df['MACD_SP500'].ffill().bfill()
    df['Signal_Line_SP500'] = df['Signal_Line_SP500'].ffill().bfill()

    # 檢查填充後的數據長度
    print(f"合併後數據集的總長度: {len(df)}")

    # 找出仍然存在 NaN 值的行
    nan_columns = df[['MACD_TSMC', 'Signal_Line_TSMC', 'MACD_SP500', 'Signal_Line_SP500']].isna()
    if nan_columns.any().any():
        print("存在未填充的 NaN 值：")
        print(df[nan_columns.any(axis=1)])  # 打印包含 NaN 值的行
        
        # 移除含有 NaN 值的行
        df = df.dropna(subset=['MACD_TSMC', 'Signal_Line_TSMC', 'MACD_SP500', 'Signal_Line_SP500'])
        print(f"移除 NaN 後數據集的總長度: {len(df)}")

    # 檢查數據量是否足夠
    if len(df) < 2:
        print("數據不足以進行預測，請檢查數據來源和處理方式。")
    else:
        # 建立 Prophet 模型
        model = Prophet(daily_seasonality=True, seasonality_mode='multiplicative', changepoint_prior_scale=0.1)
        model.add_regressor('MACD_TSMC')
        model.add_regressor('Signal_Line_TSMC')
        model.add_regressor('MACD_SP500')
        model.add_regressor('Signal_Line_SP500')

        # 訓練 Prophet 模型
        model.fit(df)

        # 建立未來 180 天的日期
        future = model.make_future_dataframe(periods=180)
        future['MACD_TSMC'] = df['MACD_TSMC'].iloc[-1]
        future['Signal_Line_TSMC'] = df['Signal_Line_TSMC'].iloc[-1]
        future['MACD_SP500'] = df['MACD_SP500'].iloc[-1]
        future['Signal_Line_SP500'] = df['Signal_Line_SP500'].iloc[-1]

        # 預測未來的股票價格
        forecast = model.predict(future)

        # 提取實際收盤價和預測數據
        actual_data = df[['ds', 'y']]  # 使用收盤價
        forecast_filtered = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]  # 預測數據

        # 合併實際和預測數據
        combined_data = pd.merge(actual_data, forecast_filtered, on='ds', how='left')

        # 顯示預測結果
        print(combined_data.tail(180))  # 只顯示最後 180 天的預測結果

        # 保存數據到 CSV 文件
        combined_data.to_csv(r'C:\Users\jenny\Downloads\stock_forecast_with_close_price_filtered.csv', index=False)
        print("預測結果已保存到 'C:\\Users\\jenny\\Downloads\\stock_forecast_with_close_price_filtered.csv'")

except Exception as e:
    print(f"數據下載失敗：{e}")
