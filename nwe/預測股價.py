import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.losses import Huber
import plotly.graph_objects as go
import time

# 1. 獲取股票數據
ticker = '2330.TW'  # 台積電
data = yf.download(ticker, start='2000-01-01', end='2024-12-31')  # 增加數據範圍
if data.empty:
    raise ValueError(f"無法下載股票數據，請確認股票代號 '{ticker}' 是否正確。")

# 2. 特徵工程
data = data[['Close', 'High', 'Low', 'Volume']].rename(columns={"Close": "Price"}).dropna()

# 移動平均線
data['MA_10'] = data['Price'].rolling(window=10).mean()
data['MA_50'] = data['Price'].rolling(window=50).mean()

# RSI 指標
delta = data['Price'].diff()
gain = delta.where(delta > 0, 0).rolling(window=14).mean()
loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

# MACD 指標
data['MACD'] = data['Price'].ewm(span=12, adjust=False).mean() - data['Price'].ewm(span=26, adjust=False).mean()

# ATR (Average True Range)
high_low = data['High'] - data['Low']
high_close = abs(data['High'] - data['Price'].shift())
low_close = abs(data['Low'] - data['Price'].shift())
true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
data['ATR'] = true_range.rolling(window=14).mean()

# 布林帶
data['Bollinger_Upper'] = data['Price'].rolling(window=20).mean() + 2 * data['Price'].rolling(window=20).std()
data['Bollinger_Lower'] = data['Price'].rolling(window=20).mean() - 2 * data['Price'].rolling(window=20).std()

# 成交量均值
data['Volume_MA_10'] = data['Volume'].rolling(window=10).mean()

# 移除 NaN 值
data = data.dropna()

# 3. 數據標準化
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data[['Price', 'MA_10', 'MA_50', 'RSI', 'MACD', 'ATR', 'Bollinger_Upper', 'Bollinger_Lower', 'Volume_MA_10']])

# 4. 構建訓練資料集
look_back = 30
X, y = [], []
for i in range(look_back, len(scaled_data)):
    X.append(scaled_data[i-look_back:i])
    y.append(scaled_data[i, 0])

X, y = np.array(X), np.array(y)

# 5. 建立 LSTM 模型
model = Sequential([
    Bidirectional(LSTM(128, return_sequences=True, input_shape=(X.shape[1], X.shape[2]))),
    Dropout(0.2),
    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.2),
    Bidirectional(LSTM(32)),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer='adam', loss=Huber(delta=1.0))

# 動態學習率調整與早停條件
reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, min_lr=1e-6)
early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
model.fit(X, y, epochs=100, batch_size=32, callbacks=[reduce_lr, early_stopping], verbose=1)

# 6. 預測未來15天的價格
def predict_next_days(model, scaled_data, look_back, future_days):
    predictions = []
    input_seq = scaled_data[-look_back:]
    for step in range(future_days):
        start_time = time.time()
        input_seq = np.expand_dims(input_seq, axis=0)
        predicted_scaled = model.predict(input_seq, verbose=0)
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
train_size = int(len(data) * 0.7)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]
predicted_prices = model.predict(X_test, verbose=0)
predicted_prices = scaler.inverse_transform(np.hstack([predicted_prices, np.zeros((len(predicted_prices), X.shape[2] - 1))]))[:, 0]

# 修正實際價格數據的維度
actual_prices = data['Price'][-len(predicted_prices):].values.flatten()

# 繪製圖表
fig = go.Figure()

# 添加實際價格曲線
fig.add_trace(go.Scatter(
    x=data.index[-len(predicted_prices):],
    y=actual_prices,
    mode='lines',
    name='Actual Price'
))

# 添加預測價格曲線
fig.add_trace(go.Scatter(
    x=data.index[-len(predicted_prices):],
    y=predicted_prices,
    mode='lines',
    name='Predicted Price'
))

# 添加未來15天的預測價格
future_dates = pd.date_range(start=data.index[-1], periods=future_days + 1)[1:]
fig.add_trace(go.Scatter(
    x=future_dates,
    y=future_prices,
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




# 8. 股票回測
def backtest(data, predicted_prices, initial_balance=1000000):
    # 初始化回測參數
    balance = initial_balance  # 初始資金
    shares = 0  # 持有的股票數量
    portfolio_value = []  # 資產價值時間序列
    actions = []  # 交易行為記錄

    for i in range(len(predicted_prices) - 1):
        # 當前實際價格與預測價格
        current_price = data['Price'].iloc[i]
        next_predicted_price = predicted_prices[i + 1]

        # 買入信號：預測價格上漲
        if next_predicted_price > current_price:
            # 買入股票（全倉）
            if balance > 0:
                shares = balance // current_price
                balance -= shares * current_price
                actions.append(f"買入 {shares} 股，價格 {current_price:.2f}")
        
        # 賣出信號：預測價格下跌
        elif next_predicted_price < current_price:
            # 賣出股票
            if shares > 0:
                balance += shares * current_price
                actions.append(f"賣出 {shares} 股，價格 {current_price:.2f}")
                shares = 0

        # 計算當前資產價值
        portfolio_value.append(balance + shares * current_price)

    # 計算回測績效指標
    final_balance = balance + shares * data['Price'].iloc[-1]
    total_return = (final_balance - initial_balance) / initial_balance
    max_drawdown = max(1 - np.array(portfolio_value) / np.maximum.accumulate(portfolio_value))
    sharpe_ratio = total_return / np.std(portfolio_value) if np.std(portfolio_value) != 0 else 0

    return {
        "Final Balance": final_balance,
        "Total Return": total_return,
        "Max Drawdown": max_drawdown,
        "Sharpe Ratio": sharpe_ratio,
        "Portfolio Value": portfolio_value,
        "Actions": actions,
    }

# 執行回測
backtest_results = backtest(data.iloc[-len(predicted_prices):], predicted_prices)

# 打印回測結果
print("回測結果：")
print(f"最終資產價值：{backtest_results['Final Balance']:.2f}")
print(f"總回報率：{backtest_results['Total Return']:.2%}")
print(f"最大回撤：{backtest_results['Max Drawdown']:.2%}")
print(f"夏普比率：{backtest_results['Sharpe Ratio']:.2f}")

# 繪製資產價值變化圖
fig_backtest = go.Figure()
fig_backtest.add_trace(go.Scatter(
    y=backtest_results['Portfolio Value'],
    mode='lines',
    name='Portfolio Value'
))
fig_backtest.update_layout(
    title='Portfolio Value Over Time',
    xaxis_title='Time',
    yaxis_title='Portfolio Value',
    template='plotly_white'
)
fig_backtest.show()
