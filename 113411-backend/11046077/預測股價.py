import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ReduceLROnPlateau
import plotly.graph_objects as go
import time

# 1. 獲取股票數據
ticker = '2330.TW'  # 台積電
data = yf.download(ticker, start='2020-01-01', end='2024-12-31')
data = data[['Close']]  # 僅保留收盤價
data = data.rename(columns={"Close": "Price"})

# 2. 特徵工程
data['MA_10'] = data['Price'].rolling(window=10).mean()
data['MA_50'] = data['Price'].rolling(window=50).mean()

# RSI
delta = data['Price'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

# MACD
data['MACD'] = data['Price'].ewm(span=12, adjust=False).mean() - data['Price'].ewm(span=26, adjust=False).mean()

# 布林帶
data['Bollinger_Upper'] = data['Price'].rolling(window=20).mean() + (data['Price'].rolling(window=20).std() * 2)
data['Bollinger_Lower'] = data['Price'].rolling(window=20).mean() - (data['Price'].rolling(window=20).std() * 2)

# 移除 NaN 值
data = data.dropna()

# 3. 數據標準化
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data[['Price', 'MA_10', 'MA_50', 'RSI', 'MACD', 'Bollinger_Upper', 'Bollinger_Lower']])

# 4. 構建訓練資料集
look_back = 30
X, y = [], []
for i in range(look_back, len(scaled_data)):
    X.append(scaled_data[i-look_back:i])
    y.append(scaled_data[i, 0])

X, y = np.array(X), np.array(y)

# 5. 建立 LSTM 模型
model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    Dropout(0.2),
    LSTM(64, return_sequences=True),
    Dropout(0.2),
    LSTM(32),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# 動態學習率調整
reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, min_lr=1e-6)
model.fit(X, y, epochs=50, batch_size=16, callbacks=[reduce_lr])

# 6. 預測未來15天的價格
def predict_next_days(model, scaled_data, look_back, future_days):
    predictions = []
    input_seq = scaled_data[-look_back:]
    for step in range(future_days):
        start_time = time.time()  # 記錄開始時間
        input_seq = np.expand_dims(input_seq, axis=0)
        predicted_scaled = model.predict(input_seq)
        # 更新所有特徵
        new_row = np.hstack([predicted_scaled[0], input_seq[0, -1, 1:]])
        input_seq = np.vstack([input_seq[0, 1:], new_row])
        predictions.append(predicted_scaled[0, 0])
        print(f"Step {step + 1}/{future_days} completed in {time.time() - start_time:.2f} seconds")
    return predictions

future_days = 15
future_scaled_prices = predict_next_days(model, scaled_data, look_back, future_days)
future_prices = scaler.inverse_transform(
    np.hstack([np.array(future_scaled_prices).reshape(-1, 1), scaled_data[-1, 1:].reshape(1, -1).repeat(future_days, axis=0)])
)[:, 0]

# 打印未來15天的預測價格
print("未來15天的預測價格：")
print(future_prices)

# 7. 模型預測價格序列（歷史數據 vs 預測數據）
train_size = int(len(data) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]
predicted_prices = model.predict(X_test)
predicted_prices = scaler.inverse_transform(np.hstack([predicted_prices, np.zeros((len(predicted_prices), 6))]))[:, 0]

# 修正實際價格數據的維度
actual_prices = data['Price'][-len(predicted_prices):]

# 確保 actual_prices 是一維數據
actual_prices = actual_prices.values.flatten()  # 將數據展平為一維

# 繪製圖表
fig = go.Figure()

# 添加實際價格曲線
fig.add_trace(go.Scatter(
    x=data['Price'][-len(predicted_prices):].index,  # 使用實際價格的索引
    y=actual_prices,                                # 修正後的一維數據
    mode='lines',
    name='Actual Price'
))

# 添加預測價格曲線
fig.add_trace(go.Scatter(
    x=data['Price'][-len(predicted_prices):].index,  # 使用相同的索引
    y=predicted_prices,                             # 預測價格
    mode='lines',
    name='Predicted Price'
))

# 添加未來15天的預測價格
future_dates = pd.date_range(start=data.index[-1], periods=future_days + 1)[1:]
fig.add_trace(go.Scatter(
    x=future_dates[::2],  # 每隔2天顯示一次
    y=future_prices[::2],
    mode='lines+markers',
    name='Future Predictions'
))

# 配置圖表佈局
fig.update_layout(
    title='Actual vs Predicted Price and Future Predictions',
    xaxis_title='Date',
    yaxis_title='Price',
    legend=dict(x=0, y=1),
    template='plotly_white'
)

fig.show()
