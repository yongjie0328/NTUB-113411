
### 設定想要的股票代碼資訊，以及要下載股價資訊的時間範圍
stock_name = '2330.TW'
start = datetime.datetime(2024, 1, 1)
end = datetime.datetime(2024, 4, 25)

### 下載股價資訊
df_full = pdr.get_data_yahoo(stock_name, start=start, end=end).reset_index()
df_full.to_csv(stock_name+'.csv',index=False)

### 看一下前幾筆資料長什麼樣子
df_full.head()
### 畫出股價資訊 2019/01/01~2020/06/14
df_full.set_index('Date', inplace=True)
df_raw = df_full[df_full.columns[-1]]
df_raw.plot(label=stock_name, figsize=(16,8), title=df_full.columns[-1], grid=True, legend=True)
window = 20
df_MA = df_full[df_full.columns[-1]].rolling(window).mean()
df_raw.plot(label=stock_name, figsize=(16,8), title=df_full.columns[-1], grid=True, legend=True)
df_MA.plot(label=stock_name+'_MA', figsize=(16,8), title=df_full.columns[-1], grid=True, legend=True)
### X 只拿第 1 天到第 N-1 天，而 y 則取第 2 天到第 N 天
df_X = df_full.iloc[:-1,:-1]
df_y = df_full.iloc[1:,-1]

X = df_X.to_numpy() 
y = df_y.to_numpy() 

### 訓練/測試的資料分割，以前 80% 的天數資料做訓練，後 20% 來做測試
num_data = df_X.shape[0]
split_ratio = 0.8
ind_split = int(split_ratio * num_data)

X_train = X[:ind_split]
y_train = y[:ind_split].reshape(-1,1)
X_test = X[ind_split:]
y_test = y[ind_split:].reshape(-1,1)

split_time = df_X.index[ind_split]
# 建立線性迴歸模型
### 訓練模型
reg_linear = LinearRegression()
reg_linear.fit(X_train, y_train)

### 將訓練好的模型，用來做預測
trainings = reg_linear.predict(X_train).reshape(-1,1)
predictions = reg_linear.predict(X_test).reshape(-1,1)

### 將預測結果合再一起
all_pred = np.concatenate((trainings, predictions), axis=0)

### 計算方均根差
train_rmse = np.sqrt(1/X_train.shape[0]*np.squeeze(np.dot((trainings - y_train).T, (trainings - y_train))))
test_rmse = np.sqrt(1/X_test.shape[0]*np.squeeze(np.dot((predictions - y_test).T, (predictions - y_test))))

print("Training RMSE is: %f" % train_rmse)
print("Testing RMSE is: %f" % test_rmse)
### 將預測和真實的股價，放進 df_linear 以便做圖
df_linear = pd.DataFrame(all_pred, columns=['Linear '+df_full.columns[-1]], index=df_y.index)
df_linear[df_full.columns[-1]] = y

### 畫出結果
df_linear.plot(figsize=(16,8), title=df_full.columns[-1], grid=True, legend=True, color=['r','C0'])
plt.axvline(pd.Timestamp(split_time),color='orange')