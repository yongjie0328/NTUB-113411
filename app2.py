from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
import yfinance as yf
from stocker import Stocker  # Assuming you have this custom module
from datetime import datetime
import io
import matplotlib
import matplotlib.pyplot as plt
import pandas_ta as ta
import numpy as np

# Use a non-interactive backend for matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
# Enable CORS for the entire app with specified origins and methods
CORS(app, resources={r"/*": {"origins": ["http://192.168.50.15:8080", "http://localhost:8080"]}}, methods=['GET', 'POST', 'OPTIONS'])

# Define global stock list
stock_list = {
    '2888.TW': '新光金控',
    '2891.TW': '中信金控',
    '2883.TW': '開發金控',
    '2882.TW': '國泰金控',
    '2867.TW': '三商壽',
    '2884.TW': '玉山金控',
    '2880.TW': '華南金控',
    '2890.TW': '永豐金控',
    '2834.TW': '臺企銀',
    '2885.TW': '元大金控',
    '2303.TW': '聯電',
    '2363.TW': '矽統',
    '2330.TW': '台積電',
    '6770.TW': '力積電',
    '2344.TW': '華邦電',
    '2449.TW': '京元電子',
    '4967.TW': '十銓科技',
    '2408.TW': '南亞科',
    '3450.TW': '聯鈞',
    '3711.TW': '日月光投控',
    '2618.TW': '長榮航',
    '2609.TW': '陽明海運',
    '2610.TW': '華航',
    '2603.TW': '長榮海運',
    '2615.TW': '萬海航運',
    '2605.TW': '新興航運',
    '2634.TW': '漢翔',
    '2606.TW': '裕民航運',
    '5608.TW': '四維航運',
    '2637.TW': '慧洋海運',
    '3231.TW': '緯創',
    '2353.TW': '宏碁',
    '2382.TW': '廣達電腦',
    '2356.TW': '英業達',
    '3013.TW': '晟銘電',
    '2324.TW': '仁寶電腦',
    '2301.TW': '光寶科技',
    '2365.TW': '昆盈',
    '3017.TW': '奇鋐',
    '3706.TW': '神達',
    '2323.TW': '中環',
    '2349.TW': '錸德',
    '2374.TW': '佳能',
    '2393.TW': '億光',
    '2406.TW': '國碩',
    '2409.TW': '友達光電',
    '2426.TW': '鼎元',
    '2429.TW': '銘旺科',
    '2438.TW': '翔耀',
    '2466.TW': '冠西電'
}

# Function to create stock prediction
def create_stock_prediction(ticker, days=90):
    df = yf.Ticker(ticker).history(period="max")
    price = df['Close']
    df.index = pd.to_datetime(df.index).tz_localize(None)

    stock = Stocker(price)
    model, model_data = stock.create_prophet_model(days=days)

    today = pd.to_datetime(datetime.now().date())
    predictions_next_30_days = model_data[model_data['ds'] >= today].head(30)

    return predictions_next_30_days[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]


def filter_non_trading_days(predictions):
    # Convert prediction dates to pandas datetime
    predictions['ds'] = pd.to_datetime(predictions['ds'])

    # Filter out weekends
    trading_days = predictions[predictions['ds'].dt.weekday < 5]

    # Additional custom market holidays (example list)
    holidays = pd.to_datetime([
        '2024-10-05',  
        '2024-10-06',  
        '2024-10-10',  
        '2024-10-12',  
        '2024-10-13',  
        '2024-10-19',  
        '2024-10-20',  
        '2024-10-26',  
        '2024-10-27',  
        '2024-11-02',  
        '2024-11-03',  
        '2024-11-09',  
        '2024-11-10',  
        '2024-11-16',  
        '2024-11-17',  
        '2024-11-23',  
        '2024-11-24',  
        '2024-11-30',  
        '2024-12-01',  
        '2024-12-07',  
        '2024-12-08',  
        '2024-12-14',  
        '2024-12-15',  
        '2024-12-21',  
        '2024-12-22',  
        '2024-12-28',  
        '2024-12-29',  
        
    ])

    # Exclude custom holidays
    trading_days = trading_days[~trading_days['ds'].isin(holidays)]

    return trading_days




# Function to calculate VaR

def calculate_var(returns, confidence_level=0.95):
    if len(returns) == 0:
        return None
    sorted_returns = sorted(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    return sorted_returns[index]

@app.route('/stock-list', methods=['GET'])
def get_stock_list():
    return jsonify(stock_list)

@app.route('/predict', methods=['GET'])
def predict_stock():
    ticker = request.args.get('ticker', '2330.TW')

    if ticker not in stock_list:
        return jsonify({'error': 'Stock not found in the provided list.'}), 400

    days = int(request.args.get('days', 90))
    try:
        # Create stock predictions as a DataFrame
        predictions_df = create_stock_prediction(ticker, days)
        
        # Filter out non-trading days
        filtered_predictions = filter_non_trading_days(predictions_df)
        
        # Convert to dictionary format for JSON response
        filtered_predictions_dict = filtered_predictions[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records')
        
        return jsonify(filtered_predictions_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/current-price', methods=['GET'])
def current_price():
    ticker = request.args.get('ticker', '2330.TW')

    if ticker not in stock_list:
        return jsonify({'error': 'Stock not found in the provided list.'}), 400

    try:
        # 嘗試獲取當前的股價
        df = yf.Ticker(ticker).history(period="1d")
        if df.empty:
            # 如果沒有找到當天數據，嘗試獲取過去5天的數據並使用最後一個有效值
            df = yf.Ticker(ticker).history(period="5d")
        
        # 檢查數據是否為空
        if df.empty:
            return jsonify({'error': f'No price data found for {ticker}. It may be delisted or not traded recently.'}), 404

        current_price = df['Close'].iloc[-1]
        return jsonify({'currentPrice': current_price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/predict-image', methods=['GET'])
def predict_image():
    ticker = request.args.get('ticker', '2330.TW')
    days = int(request.args.get('days', 90))

    if ticker not in stock_list:
        return jsonify({'error': 'Stock not found in the provided list.'}), 400

    try:
        df = yf.Ticker(ticker).history(period="max")
        price = df['Close']
        df.index = pd.to_datetime(df.index).tz_localize(None)

        stock = Stocker(price)
        model, model_data = stock.create_prophet_model(days=days)

        today = pd.to_datetime(datetime.now().date())
        start_of_year = pd.to_datetime(datetime(today.year, 1, 1))

        actual_stock_this_year = df[df.index >= start_of_year]
        predicted_stock_this_year = model_data[model_data['ds'] >= start_of_year]

        plt.figure(figsize=(10, 6))
        plt.plot(actual_stock_this_year.index, actual_stock_this_year['Close'], label='Actual Price', color='black')
        plt.plot(predicted_stock_this_year['ds'], predicted_stock_this_year['yhat'], label='Predicted Price', color='blue')
        plt.fill_between(predicted_stock_this_year['ds'], predicted_stock_this_year['yhat_lower'], predicted_stock_this_year['yhat_upper'], color='lightblue', alpha=0.5, label='Confidence Interval')
        plt.xlabel('Date')
        plt.ylabel('Price $')
        plt.title(f'{ticker} Stock Price Prediction (This Year)')
        plt.legend()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return send_file(img, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculate_portfolio', methods=['POST', 'OPTIONS'])
def calculate_portfolio():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200

    data = request.json
 
    selected_tickers = data['tickers']
    investment_distribution = data['proportions']
    investment_amount = float(data['investment_amount'])

    # Validate investment amount
    if investment_amount <= 0:
        return jsonify({'error': 'Investment amount must be positive.'}), 400

    # Validate proportions
    if not all(0 <= p <= 1 for p in investment_distribution.values()):
        return jsonify({'error': 'Proportions must be between 0 and 1.'}), 400

    total_proportion = sum(investment_distribution.values())
    if not np.isclose(total_proportion, 1.0):
        return jsonify({'error': 'Total proportions must sum to 1.'}), 400

    stock_data = {}
    results = {}

    for ticker in selected_tickers:
        try: 
            stock_data[ticker] = yf.download(ticker, start='2023-01-01', end='2024-10-04')
            # 嘗試獲取即時股價
            current_price_data = yf.Ticker(ticker).history(period='1d')

            if current_price_data.empty:
                # 如果當天的數據為空，獲取最近5天內的最後一個可用收盤價
                current_price_data = yf.Ticker(ticker).history(period='5d')

            # 再次檢查數據是否可用
            if not current_price_data.empty:
                current_price = current_price_data['Close'].iloc[-1]
            else:
                current_price = None  # 或者設置為某個默認值，如 0
            
            company_name = stock_list.get(ticker, ticker)
            data = stock_data[ticker]
            data['RSI'] = ta.rsi(data['Close'])
            data['MA_50'] = ta.sma(data['Close'], length=50)
            data['MA_200'] = ta.sma(data['Close'], length=200)

            macd = ta.macd(data['Close'])
            data['MACD'] = macd['MACD_12_26_9']
            data['MACD_signal'] = macd['MACDs_12_26_9']
            data['MACD_hist'] = macd['MACDh_12_26_9']

            stochastic = ta.stoch(data['High'], data['Low'], data['Close'])
            data['Stochastic_K'] = stochastic['STOCHk_14_3_3']
            data['Stochastic_D'] = stochastic['STOCHd_14_3_3']

            ticker_info = yf.Ticker(ticker).info
            financials = {
                'market_cap': ticker_info.get('marketCap'),
                'price_to_earnings': ticker_info.get('trailingPE'),
                'revenue': ticker_info.get('totalRevenue'),
                'gross_profit': ticker_info.get('grossProfits', "無數據"),
                'debt_to_equity': ticker_info.get('debtToEquity')
            }
        except Exception as e:
            # 處理其他可能的錯誤
            print(f"Error fetching data for {ticker}: {e}")
            current_price = None  # 或者設置為某個默認值，如 0
            
            # 在此處設置一個默認的 financials 值
            financials = {
                'market_cap': "無數據",
                'price_to_earnings': "無數據",
                'revenue': "無數據",
                'gross_profit': "無數據",
                'debt_to_equity': "無數據"
            }

        results[ticker] = {
            'company_name': company_name,
            'current_price': current_price,
            'technical_analysis': {
                'RSI': data['RSI'].iloc[-1] if not data['RSI'].empty else "無數據",
                'MA_50': data['MA_50'].iloc[-1] if not data['MA_50'].empty else "無數據",
                'MA_200': data['MA_200'].iloc[-1] if not data['MA_200'].empty else "無數據",
                'MACD': data['MACD'].iloc[-1] if not data['MACD'].empty else "無數據",
                'MACD_signal': data['MACD_signal'].iloc[-1] if not data['MACD_signal'].empty else "無數據",
                'MACD_hist': data['MACD_hist'].iloc[-1] if not data['MACD_hist'].empty else "無數據",
                'Stochastic_K': data['Stochastic_K'].iloc[-1] if not data['Stochastic_K'].empty else "無數據",
                'Stochastic_D': data['Stochastic_D'].iloc[-1] if not data['Stochastic_D'].empty else "無數據"
            },
            'financials': financials
        }
        
    
    returns = pd.concat([stock_data[ticker]['Adj Close'].pct_change() for ticker in selected_tickers], axis=1)
    returns.columns = selected_tickers
    returns = returns.dropna()

    weights = np.array([investment_distribution[ticker] for ticker in selected_tickers])

    cov_matrix = returns.cov()
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_volatility = np.sqrt(portfolio_variance)

    annual_returns = returns.mean() * 252
    portfolio_return = np.dot(annual_returns, weights)

    z_score = 1.96
    potential_loss = investment_amount * portfolio_volatility * z_score
    expected_gain = investment_amount * portfolio_return

    portfolio_returns = np.dot(returns, weights)
    var_percentage = calculate_var(portfolio_returns, confidence_level=0.95)
    var_amount = investment_amount * var_percentage

    return jsonify({
        'portfolio_volatility_percentage': portfolio_volatility * 100,
        'portfolio_return_percentage': portfolio_return * 100,
        'potential_loss': potential_loss,
        'expected_gain': expected_gain,
        'var_percentage': var_percentage * 100,
        'var_amount': var_amount,
        'detailed_analysis': results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
