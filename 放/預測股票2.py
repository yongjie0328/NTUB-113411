import yfinance as yf
import pandas as pd
from prophet import Prophet

# RSI 計算
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# KD 指標計算
def calculate_kd(df, n=9):
    low_min = df['Low_TSMC'].rolling(window=n, min_periods=1).min()
    high_max = df['High_TSMC'].rolling(window=n, min_periods=1).max()
    df['RSV'] = (df['y'] - low_min) / (high_max - low_min) * 100
    df['K'] = df['RSV'].ewm(com=2, min_periods=1).mean()  # 初始 K 值使用 RSV 的平滑
    df['D'] = df['K'].ewm(com=2, min_periods=1).mean()  # 初始 D 值使用 K 值的平滑
    return df

# 設置時間範圍
start_date = "2010-01-01"
end_date = "2024-09-28"

try:
    # 下載台積電的股價數據 (台積電代碼: 2330.TW)
    tsmc = yf.Ticker("2330.TW")
    tsmc_data = tsmc.history(start=start_date, end=end_date)
    
    # 檢查台積電數據是否成功下載
    if tsmc_data.empty:
        raise ValueError("無法下載台積電的數據，請檢查股票代碼和日期範圍。")

    # 下載台股加權指數數據 (代碼: ^TWII)
    twii = yf.Ticker("^TWII")
    twii_data = twii.history(start=start_date, end=end_date)

    # 檢查台股加權指數數據是否成功下載
    if twii_data.empty:
        raise ValueError("無法下載台股加權指數的數據，請檢查指數代碼和日期範圍。")

    # 合併台積電和台股加權指數的數據，只保留兩者都有交易的日期
    df = tsmc_data.reset_index().merge(twii_data.reset_index(), on='Date', how='inner', suffixes=('_TSMC', '_TWII'))
    df['Date'] = df['Date'].dt.tz_localize(None)  # 去除時區信息
    df.rename(columns={'Date': 'ds', 'Close_TSMC': 'y'}, inplace=True)  # Prophet 要求的列名稱

    # 計算 MACD 和信號線
    df['EMA_12_TSMC'] = df['y'].ewm(span=12, adjust=False).mean()
    df['EMA_26_TSMC'] = df['y'].ewm(span=26, adjust=False).mean()
    df['MACD_TSMC'] = df['EMA_12_TSMC'] - df['EMA_26_TSMC']
    df['Signal_Line_TSMC'] = df['MACD_TSMC'].ewm(span=9, adjust=False).mean()

    df['EMA_12_TWII'] = df['Close_TWII'].ewm(span=12, adjust=False).mean()
    df['EMA_26_TWII'] = df['Close_TWII'].ewm(span=26, adjust=False).mean()
    df['MACD_TWII'] = df['EMA_12_TWII'] - df['EMA_26_TWII']
    df['Signal_Line_TWII'] = df['MACD_TWII'].ewm(span=9, adjust=False).mean()

    # 計算 RSI
    df['RSI_TSMC'] = calculate_rsi(df['y'], period=14)
    df['RSI_TWII'] = calculate_rsi(df['Close_TWII'], period=14)

    # 計算 MA (移動平均線)
    df['MA_20_TSMC'] = df['y'].rolling(window=20).mean()
    df['MA_20_TWII'] = df['Close_TWII'].rolling(window=20).mean()

    # 計算 KD 指標
    df = calculate_kd(df)

    # 填充 NaN 值
    df['MACD_TSMC'] = df['MACD_TSMC'].ffill().bfill()
    df['Signal_Line_TSMC'] = df['Signal_Line_TSMC'].ffill().bfill()
    df['MACD_TWII'] = df['MACD_TWII'].ffill().bfill()
    df['Signal_Line_TWII'] = df['Signal_Line_TWII'].ffill().bfill()
    df['RSI_TSMC'] = df['RSI_TSMC'].ffill().bfill()
    df['RSI_TWII'] = df['RSI_TWII'].ffill().bfill()
    df['MA_20_TSMC'] = df['MA_20_TSMC'].ffill().bfill()
    df['MA_20_TWII'] = df['MA_20_TWII'].ffill().bfill()
    df['K'] = df['K'].ffill().bfill()
    df['D'] = df['D'].ffill().bfill()

    # 檢查填充後的數據長度
    print(f"合併後數據集的總長度: {len(df)}")

    # 移除仍然存在 NaN 值的行
    df.dropna(subset=['MACD_TSMC', 'Signal_Line_TSMC', 'MACD_TWII', 'Signal_Line_TWII', 'RSI_TSMC', 'RSI_TWII', 'MA_20_TSMC', 'MA_20_TWII', 'K', 'D'], inplace=True)
    print(f"移除 NaN 後數據集的總長度: {len(df)}")

    # 檢查數據量是否足夠
    if len(df) < 2:
        print("數據不足以進行預測，請檢查數據來源和處理方式。")
    else:
        # 建立 Prophet 模型
        model = Prophet(daily_seasonality=True, seasonality_mode='multiplicative', changepoint_prior_scale=0.1)
        model.add_regressor('MACD_TSMC')
        model.add_regressor('Signal_Line_TSMC')
        model.add_regressor('MACD_TWII')
        model.add_regressor('Signal_Line_TWII')
        model.add_regressor('RSI_TSMC')
        model.add_regressor('RSI_TWII')
        model.add_regressor('MA_20_TSMC')
        model.add_regressor('MA_20_TWII')
        model.add_regressor('K')
        model.add_regressor('D')

        # 訓練 Prophet 模型
        model.fit(df)

        # 建立未來 180 天的日期
        future = model.make_future_dataframe(periods=30)
        future['MACD_TSMC'] = df['MACD_TSMC'].iloc[-1]
        future['Signal_Line_TSMC'] = df['Signal_Line_TSMC'].iloc[-1]
        future['MACD_TWII'] = df['MACD_TWII'].iloc[-1]
        future['Signal_Line_TWII'] = df['Signal_Line_TWII'].iloc[-1]
        future['RSI_TSMC'] = df['RSI_TSMC'].iloc[-1]
        future['RSI_TWII'] = df['RSI_TWII'].iloc[-1]
        future['MA_20_TSMC'] = df['MA_20_TSMC'].iloc[-1]
        future['MA_20_TWII'] = df['MA_20_TWII'].iloc[-1]
        future['K'] = df['K'].iloc[-1]
        future['D'] = df['D'].iloc[-1]

        # 預測未來的股票價格
        forecast = model.predict(future)

        # 提取實際收盤價和預測數據
        actual_data = df[['ds', 'y']]  # 使用收盤價
        forecast_filtered = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]  # 預測數據

        # 合併實際和預測數據
        combined_data = pd.merge(actual_data, forecast_filtered, on='ds', how='right')

        # 將未開市的日期標記為 "未開市"
        combined_data['y'] = combined_data['y'].fillna('未開市')

        # 顯示預測結果
        print(combined_data.tail(30))  # 只顯示最後 180 天的預測結果

        # 保存數據到 CSV 文件
        combined_data.to_csv(r'C:\Users\jenny\Downloads\stock_forecast_with_technical_analysis.csv', index=False)
        print("預測結果已保存到 'C:\\Users\\jenny\\Downloads\\stock_forecast_with_technical_analysis.csv'")

except Exception as e:
    print(f"數據下載失敗：{e}")
