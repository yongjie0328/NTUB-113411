from prophet.diagnostics import cross_validation, performance_metrics
import matplotlib.pyplot as plt
from textblob import TextBlob
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib
import requests
import prophet

class Stocker():
    
    # 初始化需要一個股票代碼
    def __init__(self, price, training_years=3):
        self.symbol = 'the stock'
        self.training_years = training_years
        s = price
        stock = pd.DataFrame({'Date': s.index, 'y': s, 'ds': s.index, 'close': s, 'open': s}, index=None)

        stock['Adj. Close'] = stock['close']
        stock['Adj. Open'] = stock['open']
        
        stock['y'] = stock['Adj. Close']
        stock['Daily Change'] = stock['Adj. Close'] - stock['Adj. Open']
        
        # 指派為類別屬性的數據
        self.stock = stock.copy()
        
        # 範圍內的最小和最大日期
        self.min_date = min(stock['ds'])
        self.max_date = max(stock['ds'])
        
        # 預設參數
        self.changepoint_prior_scale = 0.05 
        self.weekly_seasonality = False
        self.daily_seasonality = False
        self.monthly_seasonality = True
        self.yearly_seasonality = True
        self.changepoints = None
        self.financial_data = None
        self.sentiment_data = None

    def add_financial_data(self, ticker):
        # 使用 yfinance 取得財務數據
        stock_info = yf.Ticker(ticker)
        
        # 取得財務訊息
        financials = stock_info.financials.transpose()
        earnings = stock_info.earnings
        
        self.financial_data = pd.DataFrame({
            'Date': financials.index,
            'Revenue': financials['Total Revenue'],
            'Earnings': earnings['Earnings']
        })
        # 標準化並與股票數據合併
        self.financial_data['Date'] = pd.to_datetime(self.financial_data['Date'])
        self.stock = pd.merge(self.stock, self.financial_data, on='Date', how='left').fillna(0)

    def fetch_news_sentiment(self, query, start_date, end_date):
        # 使用新聞 API 取得新聞資料
        api_key = '7ec6753ed8a0451bbca566c6dd043b23'
        url = f"https://newsapi.org/v2/everything?q={query}&from={start_date}&to={end_date}&apiKey={api_key}"
        
        response = requests.get(url)
        news_data = response.json()
        if '"description' not in news_data:
            print('Error fetching news data:', news_data.get('message', 'Unknown error'))
            return
        
        # 對新聞標題進行情緒分析
        sentiments = []
        dates = []
        
        for article in news_data['"description']:
            headline = article['title']
            sentiment = TextBlob(headline).sentiment.polarity
            date = pd.to_datetime(article['publishedAt']).date()
            sentiments.append(sentiment)
            dates.append(date)
        
        # 為情感資料建立 DataFrame
        sentiment_df = pd.DataFrame({'Date': dates, 'Sentiment': sentiments})
        sentiment_df = sentiment_df.groupby('Date').mean().reset_index()
        
        # 與股票數據合併
        self.sentiment_data = sentiment_df
        self.stock = pd.merge(self.stock, sentiment_df, on='Date', how='left').fillna(0)

    def create_model(self, changepoint_prior_scale=None, seasonality_mode=None):
        # 使用傳遞的參數或預設參數
        cps = changepoint_prior_scale if changepoint_prior_scale else self.changepoint_prior_scale
        sm = seasonality_mode if seasonality_mode else 'multiplicative'
        
        # 創建 Prophet 模型
        model = prophet.Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True,
            seasonality_mode=sm,
            changepoint_prior_scale=cps
        )
        
        # 添加自定義回歸變量
        if 'Revenue' in self.stock.columns:
            model.add_regressor('Revenue')
        if 'Earnings' in self.stock.columns:
            model.add_regressor('Earnings')
        if 'Sentiment' in self.stock.columns:
            model.add_regressor('Sentiment')
        
        # 添加月度季節性
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)

        return model

    def tune_model(self):
        # 設置可能的 changepoint_prior_scale 值
        changepoint_priors = [0.001, 0.01, 0.05, 0.1, 0.2]
        best_changepoint_prior = None
        best_mae = float('inf')
        
        for cps in changepoint_priors:
            model = self.create_model(changepoint_prior_scale=cps)
            model.fit(self.stock)

            # 進行交叉驗證，預測 30 天
            df_cv = cross_validation(model, initial='730 days', period='180 days', horizon='30 days')
            df_p = performance_metrics(df_cv)

            # 選擇平均絕對誤差最小的 changepoint_prior_scale
            if df_p['mae'].mean() < best_mae:
                best_mae = df_p['mae'].mean()
                best_changepoint_prior = cps

        print(f"最佳的 changepoint_prior_scale 值: {best_changepoint_prior}，MAE: {best_mae}")
        return best_changepoint_prior

    def create_prophet_model(self, days=0, resample=False):
        # 創建 Prophet 模型
        model = self.create_model()
        
        # 使用過去 self.training_years 年的數據進行預測
        stock_history = self.stock[self.stock['Date'] > (self.max_date - pd.DateOffset(years=self.training_years))].copy()
        
        if resample:
            stock_history = self.resample(stock_history)
        
        stock_history['ds'] = pd.to_datetime(stock_history['ds']).dt.tz_localize(None)
        
        # 模型訓練
        model.fit(stock_history)
        
        # 創建未来的日期框架
        future = model.make_future_dataframe(periods=days, freq='D')
        
        # 為未來數據框添加回歸變量
        if 'Revenue' in self.stock.columns:
            future['Revenue'] = self.stock['Revenue']
        if 'Earnings' in self.stock.columns:
            future['Earnings'] = self.stock['Earnings']
        if 'Sentiment' in self.stock.columns:
            future['Sentiment'] = self.stock['Sentiment']
        
        future['ds'] = pd.to_datetime(future['ds']).dt.tz_localize(None)
        future = model.predict(future)
        
        # 繪製結果
        fig, ax = plt.subplots(1, 1)
        ax.plot(stock_history['ds'], stock_history['y'], 'ko-', linewidth=1.4, alpha=0.8, ms=1.8, label='Observations')
        ax.plot(future['ds'], future['yhat'], 'forestgreen', linewidth=2.4, label='Modeled')
        ax.fill_between(future['ds'].dt.to_pydatetime(), future['yhat_upper'], future['yhat_lower'], alpha=0.3, facecolor='g', edgecolor='k', linewidth=1.4, label='Confidence Interval')
        plt.legend(loc=2, prop={'size':10})
        plt.xlabel('Date')
        plt.ylabel('Price $')
        plt.title(f'{self.symbol} Historical and Predicted Stock Price')
        plt.grid(linewidth=0.6, alpha=0.6)

        return model, future

    # 其他方法，如remove_weekends、resample等。
    # Prophet模型建立方法
    def create_model(self):
        # 製作模型
        model = prophet.Prophet(daily_seasonality=self.daily_seasonality,  
                                  weekly_seasonality=self.weekly_seasonality, 
                                  yearly_seasonality=self.yearly_seasonality,
                                  changepoint_prior_scale=self.changepoint_prior_scale,
                                  changepoints=self.changepoints)
        
        if self.monthly_seasonality:
            # 新增每月季節性
            model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        
        return model

    # 評估一年的預測模型
    def evaluate_prediction(self, start_date=None, end_date=None, nshares=None):
        # 預設開始日期是資料結束前一年
        # 預設結束日期是資料的結束日期
        if start_date is None:
            start_date = self.max_date - pd.DateOffset(years=1)
        if end_date is None:
            end_date = self.max_date

        start_date, end_date = self.handle_dates(start_date, end_date)

        # 訓練資料在開始日期前 self.training_years 開始，一直持續到開始日期
        train = self.stock[(self.stock['Date'] < start_date) &
                           (self.stock['Date'] > (start_date - pd.DateOffset(years=self.training_years)))]

        # 測試數據在指定範圍內
        test = self.stock[(self.stock['Date'] >= start_date) & (self.stock['Date'] <= end_date)]

        # 創建並訓練模型
        model = self.create_model()
        model.fit(train)

        # 做出未來的資料框和預測
        future = model.make_future_dataframe(periods=365, freq='D')
        future = model.predict(future)

        # 將預測與已知值合併
        test = pd.merge(test, future, on='ds', how='inner')
        train = pd.merge(train, future, on='ds', how='inner')

        # 計算連續測量之間的差異
        test['pred_diff'] = test['yhat'].diff()
        test['real_diff'] = test['y'].diff()

        # 正確是指我們預測的方向正確
        test['correct'] = (np.sign(test['pred_diff']) == np.sign(test['real_diff'])) * 1

        # 我們預測增加和減少時的準確性
        increase_accuracy = 100 * np.mean(test[test['pred_diff'] > 0]['correct'])
        decrease_accuracy = 100 * np.mean(test[test['pred_diff'] < 0]['correct'])

        # 計算平均絕對誤差
        test_errors = abs(test['y'] - test['yhat'])
        test_mean_error = np.mean(test_errors)

        # 計算平均絕對百分比誤差 (MAPE)
        test_mape = 100 * np.mean(test_errors / test['y'])

        # 計算均方根誤差 (RMSE)
        test_rmse = np.sqrt(np.mean(test_errors ** 2))

        # 計算 R 平方 (R²)
        ss_total = np.sum((test['y'] - np.mean(test['y'])) ** 2)
        ss_residual = np.sum((test['y'] - test['yhat']) ** 2)
        r_squared = 1 - (ss_residual / ss_total)

        # 計算時間實際值在預測範圍內的百分比
        test['in_range'] = (test['y'] < test['yhat_upper']) & (test['y'] > test['yhat_lower'])
        in_range_accuracy = 100 * np.mean(test['in_range'])

        if not nshares:
            # 預測的日期範圍
            print('\nPrediction Range: {} to {}.'.format(start_date, end_date))
            print('\nPredicted price on {} = ${:.2f}.'.format(max(future['ds']), future['yhat'].iloc[-1]))
            print('Actual price on    {} = ${:.2f}.\n'.format(max(test['ds']), test['y'].iloc[-1]))

            print('Average Absolute Error on Testing Data = ${:.2f}.'.format(test_mean_error))
            print('Mean Absolute Percentage Error (MAPE) = {:.2f}%.'.format(test_mape))
            print('Root Mean Squared Error (RMSE) = ${:.2f}.'.format(test_rmse))
            print('R-Squared (R²) = {:.4f}.'.format(r_squared))

            print('When the model predicted an increase, the price increased {:.2f}% of the time.'.format(increase_accuracy))
            print('When the model predicted a decrease, the price decreased {:.2f}% of the time.'.format(decrease_accuracy))

            print('The actual value was within the {:d}% confidence interval {:.2f}% of the time.'.format(int(100 * model.interval_width), in_range_accuracy))

            # 重製圖布
            self.reset_plot()

            # 設定圖布
            fig, ax = plt.subplots(1, 1)
            ax.plot(train['ds'], train['y'], 'ko-', linewidth=1.4, alpha=0.8, ms=1.8, label='Observations')
            ax.plot(test['ds'], test['y'], 'ko-', linewidth=1.4, alpha=0.8, ms=1.8, label='Observations')
            ax.plot(future['ds'], future['yhat'], 'navy', linewidth=2.4, label='Predicted')
            ax.fill_between(future['ds'].dt.to_pydatetime(), future['yhat_upper'], future['yhat_lower'], alpha=0.6,
                            facecolor='gold', edgecolor='k', linewidth=1.4, label='Confidence Interval')
            plt.vlines(x=min(test['ds']), ymin=min(future['yhat_lower']), ymax=max(future['yhat_upper']), colors='r',
                       linestyles='dashed', label='Prediction Start')
            plt.legend(loc=2, prop={'size': 8})
            plt.xlabel('Date')
            plt.ylabel('Price $')
            plt.title('{} Model Evaluation from {} to {}.'.format(self.symbol, start_date, end_date))
            plt.show()

        elif nshares:
            
            # 只有當我們預測股票會上漲時才投資股票
            test_pred_increase = test[test['pred_diff'] > 0]
            
            test_pred_increase.reset_index(inplace=True)
            prediction_profit = []
            
            # 迭代所有預測並計算利潤
            for i, correct in enumerate(test_pred_increase['correct']):
                
                # 如果我們預測價格上漲並且價格上漲，我們就會獲得差價
                if correct == 1:
                    prediction_profit.append(nshares * test_pred_increase['real_diff'].iloc[i])
                # 如果我們預測價格上漲而價格下跌，我們就會損失差價
                else:
                    prediction_profit.append(nshares * test_pred_increase['real_diff'].iloc[i])
            
            test_pred_increase['pred_profit'] = prediction_profit
            
            # 將利潤放入測試資料框中
            test = pd.merge(test, test_pred_increase[['ds', 'pred_profit']], on = 'ds', how = 'left')
            test['pred_profit'].iloc[0] = 0
        
            # 任一方法在所有日期的利潤
            test['pred_profit'] = test['pred_profit'].cumsum().ffill()
            test['hold_profit'] = nshares * (test['y'] - float(test['y'].iloc[0]))
            
            # 顯示訊息
            print('You played the stock market in {} from {} to {} with {} shares.\n'.format(
                self.symbol, start_date, end_date, nshares))
            
            print('When the model predicted an increase, the price increased {:.2f}% of the time.'.format(increase_accuracy))
            print('When the model predicted a  decrease, the price decreased  {:.2f}% of the time.\n'.format(decrease_accuracy))

            # 顯示一些有關股市風險的友好訊息
            print('The total profit using the Prophet model = ${:.2f}.'.format(np.sum(prediction_profit)))
            print('The Buy and Hold strategy profit =         ${:.2f}.'.format(float(test['hold_profit'].iloc[len(test) - 1])))
            print('\nThanks for playing the stock market!\n')
            
            # 繪製一段時間內的預測利潤和實際利潤
            self.reset_plot()
            
            # 用於定位文本的最終利潤
            final_profit = test['pred_profit'].iloc[len(test) - 1]
            final_smart = test['hold_profit'].iloc[len(test) - 1]

            # 文字位置
            last_date = test['ds'].iloc[len(test) - 1]
            text_location = (last_date - pd.DateOffset(months = 1))

            plt.style.use('dark_background')

            # 繪製利潤圖
            plt.plot(test['ds'], test['hold_profit'], 'b',
                     linewidth = 1.8, label = 'Buy and Hold Strategy') 

            # 繪製預測利潤
            plt.plot(test['ds'], test['pred_profit'], 
                     color = 'g' if final_profit > 0 else 'r',
                     linewidth = 1.8, label = 'Prediction Strategy')

            # 在圖表上顯示最終值
            plt.text(x = text_location, 
                     y =  final_profit + (final_profit / 40),
                     s = '$%d' % final_profit,
                    color = 'g' if final_profit > 0 else 'r',
                    size = 18)
            
            plt.text(x = text_location, 
                     y =  final_smart + (final_smart / 40),
                     s = '$%d' % final_smart,
                    color = 'g' if final_smart > 0 else 'r',
                    size = 18)

            # 繪圖格式
            plt.ylabel('Profit  (US $)'); plt.xlabel('Date'); 
            plt.title('Predicted versus Buy and Hold Profits');
            plt.legend(loc = 2, prop={'size': 10});
            plt.grid(alpha=0.2); 
            plt.show()
        
    def retrieve_google_trends(self, search, date_range):
        
        # 設定趨勢取得對象
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [search]

        try:
        
            # 建立搜尋對象
            pytrends.build_payload(kw_list, cat=0, timeframe=date_range[0], geo='', gprop='news')
            
            # 隨著時間的推移檢索利息
            trends = pytrends.interest_over_time()

            related_queries = pytrends.related_queries()

        except Exception as e:
            print('\nGoogle Search Trend retrieval failed.')
            print(e)
            return
        
        return trends, related_queries
        
    def changepoint_date_analysis(self, search=None):
        self.reset_plot()

        model = self.create_model()
        
        # 使用過去 self.training_years 年的數據
        train = self.stock[self.stock['Date'] > (self.max_date - pd.DateOffset(years = self.training_years))]
        model.fit(train)
        
        # 訓練資料的預測（無未來時期）
        future = model.make_future_dataframe(periods=0, freq='D')
        future = model.predict(future)
    
        train = pd.merge(train, future[['ds', 'yhat']], on = 'ds', how = 'inner')
        
        changepoints = model.changepoints
        train = train.reset_index(drop=True)
        
        # 僅建立變更點的資料框
        change_indices = []
        for changepoint in (changepoints):
            change_indices.append(train[train['ds'] == changepoint].index[0])
        
        c_data = train.iloc[change_indices, :]
        deltas = model.params['delta'][0]
        
        c_data['delta'] = deltas
        c_data['abs_delta'] = abs(c_data['delta'])
        
        # 依最大變化對數值進行排序
        c_data = c_data.sort_values(by='abs_delta', ascending=False)

        # 限制為 10 個最大的變化點
        c_data = c_data[:10]

        # 分為負變化點和正變化點
        cpos_data = c_data[c_data['delta'] > 0]
        cneg_data = c_data[c_data['delta'] < 0]

        # 變化點和數據
        if not search:
        
            print('\nChangepoints sorted by slope rate of change (2nd derivative):\n')
            print(c_data[['Date', 'Adj. Close', 'delta']][:5])

            # 顯示實際值、估計值和變化點的線圖
            self.reset_plot()
            
            # 設定線圖
            plt.plot(train['ds'], train['y'], 'ko', ms = 4, label = 'Stock Price')
            plt.plot(future['ds'], future['yhat'], color = 'navy', linewidth = 2.0, label = 'Modeled')
            
            # 變化點作為垂直線
            plt.vlines(cpos_data['ds'].dt.to_pydatetime(), ymin = min(train['y']), ymax = max(train['y']), 
                       linestyles='dashed', color = 'r', 
                       linewidth= 1.2, label='Negative Changepoints')

            plt.vlines(cneg_data['ds'].dt.to_pydatetime(), ymin = min(train['y']), ymax = max(train['y']), 
                       linestyles='dashed', color = 'darkgreen', 
                       linewidth= 1.2, label='Positive Changepoints')

            plt.legend(prop={'size':10});
            plt.xlabel('Date'); plt.ylabel('Price ($)'); plt.title('Stock Price with Changepoints')
            plt.show()
        
        # 在Google新聞中搜尋搜尋字詞
        # 顯示相關查詢，上升相關查詢
        # 圖表變化點、搜尋頻率、股票價格
        if search:
            date_range = ['%s %s' % (str(min(train['Date'])), str(max(train['Date'])))]

            # 取得指定術語的 Google 趨勢並加入訓練資料框
            trends, related_queries = self.retrieve_google_trends(search, date_range)

            if (trends is None)  or (related_queries is None):
                print('No search trends found for %s' % search)
                return

            print('\n Top Related Queries: \n')
            print(related_queries[search]['top'].head())

            print('\n Rising Related Queries: \n')
            print(related_queries[search]['rising'].head())

            # 將資料進行上採樣以與訓練資料連接
            trends = trends.resample('D')

            trends = trends.reset_index(level=0)
            trends = trends.rename(columns={'date': 'ds', search: 'freq'})

            # 插值頻率
            trends['freq'] = trends['freq'].interpolate()

            # 與訓練資料合併
            train = pd.merge(train, trends, on = 'ds', how = 'inner')

            # 標準化值
            train['y_norm'] = train['y'] / max(train['y'])
            train['freq_norm'] = train['freq'] / max(train['freq'])
            
            self.reset_plot()

            # 繪製標準化股票價格並標準化搜尋頻率
            plt.plot(train['ds'], train['y_norm'], 'k-', label = 'Stock Price')
            plt.plot(train['ds'], train['freq_norm'], color='goldenrod', label = 'Search Frequency')

            # 變化點作為垂直線
            plt.vlines(cpos_data['ds'].dt.to_pydatetime(), ymin = 0, ymax = 1, 
                       linestyles='dashed', color = 'r', 
                       linewidth= 1.2, label='Negative Changepoints')

            plt.vlines(cneg_data['ds'].dt.to_pydatetime(), ymin = 0, ymax = 1, 
                       linestyles='dashed', color = 'darkgreen', 
                       linewidth= 1.2, label='Positive Changepoints')

            # P批次格式化
            plt.legend(prop={'size': 10})
            plt.xlabel('Date'); plt.ylabel('Normalized Values'); plt.title('%s Stock Price and Search Frequency for %s' % (self.symbol, search))
            plt.show()
        
    # 預測給定天數範圍內的未來價格
    def predict_future(self, days=30):
        
        # 使用過去的 self.training_years 年進行訓練
        train = self.stock[self.stock['Date'] > (max(self.stock['Date']
                                                    ) - pd.DateOffset(years=self.training_years))]
        
        model = self.create_model()
        
        model.fit(train)
        
        # 具有指定預測天數的未來資料框
        future = model.make_future_dataframe(periods=days, freq='D')
        future = model.predict(future)
        
        # 只關心未來的日期
        future = future[future['ds'] >= max(self.stock['Date'])]
        
        # 去掉週末
        future = self.remove_weekends(future)
        
        # 計算是否增加
        future['diff'] = future['yhat'].diff()
    
        future = future.dropna()

        # 找到預測方向並建立單獨的資料幀
        future['direction'] = (future['diff'] > 0) * 1
        
        # 重新命名用於演示的列
        future = future.rename(columns={'ds': 'Date', 'yhat': 'estimate', 'diff': 'change', 
                                        'yhat_upper': 'upper', 'yhat_lower': 'lower'})
        
        future_increase = future[future['direction'] == 1]
        future_decrease = future[future['direction'] == 0]
        
        # 列印日期
        print('\nPredicted Increase: \n')
        print(future_increase[['Date', 'estimate', 'change', 'upper', 'lower']])
        
        print('\nPredicted Decrease: \n')
        print(future_decrease[['Date', 'estimate', 'change', 'upper', 'lower']])
        
        self.reset_plot()
        
        # 設定圖布
        plt.style.use('fivethirtyeight')
        matplotlib.rcParams['axes.labelsize'] = 10
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 8
        matplotlib.rcParams['axes.titlesize'] = 12
        
        # 繪製預測並指出是增加還是減少
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))

        # 繪製估計值
        ax.plot(future_increase['Date'], future_increase['estimate'], 'g^', ms = 12, label = 'Pred. Increase')
        ax.plot(future_decrease['Date'], future_decrease['estimate'], 'rv', ms = 12, label = 'Pred. Decrease')

        # 繪製誤差線
        ax.errorbar(future['Date'].dt.to_pydatetime(), future['estimate'], 
                    yerr = future['upper'] - future['lower'], 
                    capthick=1.4, color = 'k',linewidth = 2,
                   ecolor='darkblue', capsize = 4, elinewidth = 1, label = 'Pred with Range')

        # 繪圖格式
        plt.legend(loc = 2, prop={'size': 10});
        plt.xticks(rotation = '45')
        plt.ylabel('Predicted Stock Price (US $)');
        plt.xlabel('Date'); plt.title('Predictions for %s' % self.symbol);
        plt.show()
        
    def changepoint_prior_validation(self, start_date=None, end_date=None,changepoint_priors = [0.001, 0.05, 0.1, 0.2]):

        # 預設開始日期是資料結束前兩年
        # 預設結束日期是資料結束前一年
        if start_date is None:
            start_date = self.max_date - pd.DateOffset(years=2)
        if end_date is None:
            end_date = self.max_date - pd.DateOffset(years=1)
            
        # 轉換為 pandas 日期時間以索引資料幀
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        start_date, end_date = self.handle_dates(start_date, end_date)
                               
        # 選擇 self.training_years 年數
        train = self.stock[(self.stock['Date'] > (start_date - pd.DateOffset(years=self.training_years))) & 
        (self.stock['Date'] < start_date)]
        
        # 測試資料透過範圍指定
        test = self.stock[(self.stock['Date'] >= start_date) & (self.stock['Date'] <= end_date)]

        eval_days = (max(test['Date']) - min(test['Date'])).days
        
        results = pd.DataFrame(0, index = list(range(len(changepoint_priors))), 
            columns = ['cps', 'train_err', 'train_range', 'test_err', 'test_range'])

        print('\nValidation Range {} to {}.\n'.format(min(test['Date']),
            max(test['Date'])))
            
        # 迭代所有變化點並建立模型
        for i, prior in enumerate(changepoint_priors):
            results['cps'].iloc[i] = prior
            
            # 選擇變化點
            self.changepoint_prior_scale = prior
            
            # 建立並訓練具有指定cps的模型
            model = self.create_model()
            model.fit(train)
            future = model.make_future_dataframe(periods=eval_days, freq='D')
                
            future = model.predict(future)
            
            # 訓練結果和指標
            train_results = pd.merge(train, future[['ds', 'yhat', 'yhat_upper', 'yhat_lower']], on = 'ds', how = 'inner')
            avg_train_error = np.mean(abs(train_results['y'] - train_results['yhat']))
            avg_train_uncertainty = np.mean(abs(train_results['yhat_upper'] - train_results['yhat_lower']))
            
            results['train_err'].iloc[i] = avg_train_error
            results['train_range'].iloc[i] = avg_train_uncertainty
            
            # 測試結果和指標
            test_results = pd.merge(test, future[['ds', 'yhat', 'yhat_upper', 'yhat_lower']], on = 'ds', how = 'inner')
            avg_test_error = np.mean(abs(test_results['y'] - test_results['yhat']))
            avg_test_uncertainty = np.mean(abs(test_results['yhat_upper'] - test_results['yhat_lower']))
            
            results['test_err'].iloc[i] = avg_test_error
            results['test_range'].iloc[i] = avg_test_uncertainty

        print(results)
      
        # 訓練和測​​試平均誤差圖
        self.reset_plot()
        
        plt.plot(results['cps'], results['train_err'], 'bo-', ms = 8, label = 'Train Error')
        plt.plot(results['cps'], results['test_err'], 'r*-', ms = 8, label = 'Test Error')
        plt.xlabel('Changepoint Prior Scale'); plt.ylabel('Avg. Absolute Error ($)');
        plt.title('Training and Testing Curves as Function of CPS')
        plt.grid(color='k', alpha=0.3)
        plt.xticks(results['cps'], results['cps'])
        plt.legend(prop={'size':10})
        plt.show()
        
        self.reset_plot()

        plt.plot(results['cps'], results['train_range'], 'bo-', ms = 8, label = 'Train Range')
        plt.plot(results['cps'], results['test_range'], 'r*-', ms = 8, label = 'Test Range')
        plt.xlabel('Changepoint Prior Scale'); plt.ylabel('Avg. Uncertainty ($)');
        plt.title('Uncertainty in Estimate as Function of CPS')
        plt.grid(color='k', alpha=0.3)
        plt.xticks(results['cps'], results['cps'])
        plt.legend(prop={'size':10})
        plt.show()