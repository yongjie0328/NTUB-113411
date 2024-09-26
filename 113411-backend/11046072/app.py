from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS
import yfinance as yf
import pandas as pd
import pandas_ta as ta  # 技術分析庫
import numpy as np

app = Flask(__name__)
CORS(app)  # 啟用 CORS

# 股票代號與中文公司名稱的對應表
company_names = {
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
    '2466.TW': '冠西電',
}

def calculate_var(returns, confidence_level=0.95):
    """計算投資組合的歷史模擬法VaR"""
    if len(returns) == 0:
        return None
    sorted_returns = sorted(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    return sorted_returns[index]

@app.route('/calculate_portfolio', methods=['POST'])
def calculate_portfolio():
    data = request.json
    selected_tickers = data['tickers']
    investment_distribution = data['proportions']
    investment_amount = float(data['investment_amount'])
    
    # 抓取選定股票的數據
    stock_data = {}
    results = {}

    for ticker in selected_tickers:
        # 下載股票數據
        stock_data[ticker] = yf.download(ticker, start='2023-01-01', end='2024-09-21')

        # 提取公司名稱
        company_name = company_names.get(ticker, ticker)  # 從映射表中獲取公司名稱，若無則顯示股票代號

        # 計算技術指標
        data = stock_data[ticker]
        data['RSI'] = ta.rsi(data['Close'])
        data['MA_50'] = ta.sma(data['Close'], length=50)
        data['MA_200'] = ta.sma(data['Close'], length=200)

        # 計算 MACD
        macd = ta.macd(data['Close'])
        data['MACD'] = macd['MACD_12_26_9']
        data['MACD_signal'] = macd['MACDs_12_26_9']
        data['MACD_hist'] = macd['MACDh_12_26_9']

        # 計算 Stochastic Oscillator (KD)
        stochastic = ta.stoch(data['High'], data['Low'], data['Close'])
        data['Stochastic_K'] = stochastic['STOCHk_14_3_3']
        data['Stochastic_D'] = stochastic['STOCHd_14_3_3']

        # 獲取即時股價（最近一天的收盤價）
        current_price_data = yf.Ticker(ticker).history(period='1d')
        current_price = current_price_data['Close'].iloc[-1]

        # 提取財務數據
        ticker_info = yf.Ticker(ticker).info
        financials = {
            'market_cap': ticker_info.get('marketCap'),
            'price_to_earnings': ticker_info.get('trailingPE'),
            'revenue': ticker_info.get('totalRevenue'),
            'gross_profit': ticker_info.get('grossProfits', "無數據"),
            'debt_to_equity': ticker_info.get('debtToEquity')
        }

        # 將技術指標、即時股價和財報數據合併進結果中
        results[ticker] = {
            'company_name': company_name,
            'current_price': current_price,
            'technical_analysis': {
                'RSI': data['RSI'].iloc[-1],
                'MA_50': data['MA_50'].iloc[-1],
                'MA_200': data['MA_200'].iloc[-1],
                'MACD': data['MACD'].iloc[-1],
                'MACD_signal': data['MACD_signal'].iloc[-1],
                'MACD_hist': data['MACD_hist'].iloc[-1],
                'Stochastic_K': data['Stochastic_K'].iloc[-1],
                'Stochastic_D': data['Stochastic_D'].iloc[-1]
            },
            'financials': financials
        }

    # 投資組合的權重
    returns = pd.concat([stock_data[ticker]['Adj Close'].pct_change() for ticker in selected_tickers], axis=1)
    returns.columns = selected_tickers
    returns = returns.dropna()

    weights = np.array([investment_distribution[ticker] for ticker in selected_tickers])

    # 計算協方差矩陣
    cov_matrix = returns.cov()

    # 計算組合的波動性（標準差）
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_volatility = np.sqrt(portfolio_variance)

    # 計算投資組合的年化回報率
    annual_returns = returns.mean() * 252  # 假設一年 252 個交易日
    portfolio_return = np.dot(annual_returns, weights)

    # 假設 95% 的置信區間，Z值為1.96
    z_score = 1.96
    potential_loss = investment_amount * portfolio_volatility * z_score
    expected_gain = investment_amount * portfolio_return

    # 計算 VaR
    portfolio_returns = np.dot(returns, weights)
    var_percentage = calculate_var(portfolio_returns, confidence_level=0.95)
    var_amount = investment_amount * var_percentage

    # 返回技術分析、財報數據和計算結果，包括 VaR
    return jsonify({
        'portfolio_volatility_percentage': portfolio_volatility * 100,
        'portfolio_return_percentage': portfolio_return * 100,
        'potential_loss': potential_loss,
        'expected_gain': expected_gain,
        'var_percentage': var_percentage * 100,
        'var_amount': var_amount,
        'detailed_analysis': results  # 包含技術分析、財報數據及即時股價
    })

if __name__ == '__main__':
    app.run(debug=True)
