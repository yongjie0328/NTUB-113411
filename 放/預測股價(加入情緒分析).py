import yfinance as yf
import pandas as pd
from prophet import Prophet
from pandas.tseries.offsets import BDay

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
    
    # 下載台股加權指數數據 (代碼: ^TWII)
    twii = yf.Ticker("^TWII")
    twii_data = twii.history(start=start_date, end=end_date)

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
    df['Sentiment_TSMC'] = df['y'].pct_change().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0)).ffill().bfill()
    df['Sentiment_TWII'] = df['Close_TWII'].pct_change().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0)).ffill().bfill()

    # 檢查填充後的數據長度
    print(f"合併後數據集的總長度: {len(df)}")

    # 再次檢查是否還有 NaN 值
    nan_columns = df.columns[df.isna().any()].tolist()
    if nan_columns:
        raise ValueError(f"存在 NaN 值的列：{nan_columns}")

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
    model.add_regressor('Sentiment_TSMC')
    model.add_regressor('Sentiment_TWII')

    # 訓練 Prophet 模型
    model.fit(df)

    # 建立未來 180 個交易日的日期（排除週末）
    future_dates = pd.date_range(start=df['ds'].max(), periods=30, freq=BDay())
    future = pd.DataFrame({'ds': future_dates})
    
    # 使用最後一個交易日的外生變量值
    last_row = df.iloc[-1]
    future['MACD_TSMC'] = last_row['MACD_TSMC']
    future['Signal_Line_TSMC'] = last_row['Signal_Line_TSMC']
    future['MACD_TWII'] = last_row['MACD_TWII']
    future['Signal_Line_TWII'] = last_row['Signal_Line_TWII']
    future['RSI_TSMC'] = last_row['RSI_TSMC']
    future['RSI_TWII'] = last_row['RSI_TWII']
    future['MA_20_TSMC'] = last_row['MA_20_TSMC']
    future['MA_20_TWII'] = last_row['MA_20_TWII']
    future['K'] = last_row['K']
    future['D'] = last_row['D']
    future['Sentiment_TSMC'] = last_row['Sentiment_TSMC']
    future['Sentiment_TWII'] = last_row['Sentiment_TWII']

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
    combined_data.to_csv(r'C:\Users\jenny\Downloads\stock_forecast_with_technical_analysis_and_sentiment.csv', index=False)
    print("預測結果已保存到 'C:\\Users\\jenny\\Downloads\\stock_forecast_with_technical_analysis_and_sentiment.csv'")

except Exception as e:
    print(f"數據下載失敗：{e}")

