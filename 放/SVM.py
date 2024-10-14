import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 1. 載入台積電股價數據
#data = pd.read_csv('"C:\Users\jenny\OneDrive\桌面\smc_stock.csv"')  # 確保文件包含 'Date' 和 'Close' 欄位
#data = pd.read_csv('C:\\Users\\jenny\\OneDrive\\桌面\\tsmc_stock.csv')
data = pd.read_csv('C:/Users/jenny/OneDrive/桌面/tsmc_stock.csv', encoding='big5')


#data['Date'] = pd.to_datetime(data['Date'])
data['Date'] = pd.to_datetime(data['Date'], format='%Y年%m月%d日')

data.set_index('Date', inplace=True)

# 2. 只使用收盤價作為特徵
data['Day'] = np.arange(len(data))  # 創建一個新的特徵，代表時間順序
X = data[['Day']].values
y = data['Close'].values

# 3. 特徵標準化
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()

# 刪除包含 NaN 值的行
data.dropna(subset=['Close'], inplace=True)

# 重新設置 X 和 y
X = data[['Day']].values
y = data['Close'].values

# 進行標準化
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()


# 4. 使用 SVR 模型進行訓練
svr_model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.01)
svr_model.fit(X_scaled, y_scaled)

# 5. 預測股價
y_pred_scaled = svr_model.predict(X_scaled)
#y_pred = scaler_y.inverse_transform(y_pred_scaled)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))


# 6. 繪製預測結果
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Close'], label='Actual Stock Price')
plt.plot(data.index, y_pred, label='Predicted Stock Price', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title('TSMC Stock Price Prediction using SVR')
plt.legend()
plt.show()
