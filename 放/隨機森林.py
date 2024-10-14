import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

# 標準化特徵
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# 假設你有台積電的歷史數據文件 'TSMC_data.csv'
# 讀取數據
data = pd.read_csv('TSMC_technical_indicators_with_daily_data.csv')

# 簡單的特徵工程：添加移動平均線、RSI等
data['SMA_10'] = data['Close'].rolling(window=10).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()
data['Price_Ratio'] = data['Close'] / data['Close'].shift(1)

# 計算 RSI
def calculate_rsi(data, window=14):
    delta = data.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = calculate_rsi(data['Close'])

# 添加每日價格變動百分比
data['Price_Change_Percentage'] = data['Close'].pct_change()


# 創建標籤：1 表示上漲，0 表示下跌或不變
data['Target'] = np.where(data['Close'].shift(-1) > data['Close'], 1, 0)

# 去除NaN值
data.dropna(inplace=True)

# 選取特徵和標籤
features = ['SMA_10', 'SMA_50', 'Price_Ratio']
X = data[features]
y = data['Target']

# 拆分訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化隨機森林模型
model = RandomForestClassifier(n_estimators=100, random_state=42)

# 訓練模型
model.fit(X_train, y_train)

# 預測測試集的漲跌機率
pred_prob = model.predict_proba(X_test)[:, 1]

# 預測測試集的漲跌
pred = model.predict(X_test)

# 評估模型
print(f"Accuracy: {accuracy_score(y_test, pred)}")
print(classification_report(y_test, pred))

# 將預測結果與實際結果進行對比
results = pd.DataFrame({'Actual': y_test, 'Predicted': pred, 'Probability': pred_prob})
print(results.head())
