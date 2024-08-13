import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 假設你已經有一個包含股票數據的DataFrame
data = pd.read_csv('stock_data.csv')

# 特徵選擇
features = ['Open', 'High', 'Low', 'Volume']  # 根據你的數據進行特徵選擇
X = data[features]
y = data['Close']

# 分割數據集為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 訓練模型
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 評估模型
predictions = model.predict(X_test)
print("Mean Absolute Error:", mean_absolute_error(y_test, predictions))

# 保存模型
import joblib
joblib.dump(model, 'stock_model.pkl')


from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

# 計算預期回報率和風險矩陣
mu = expected_returns.mean_historical_return(data)
S = risk_models.sample_cov(data)

# 構建有效前沿模型
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()  # 或者使用ef.min_volatility()來最小化風險
cleaned_weights = ef.clean_weights()
print(cleaned_weights)

# 顯示投資組合績效
performance = ef.portfolio_performance(verbose=True)
