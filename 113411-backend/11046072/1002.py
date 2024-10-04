from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# 模擬公司詳細信息數據
company_data = {
    '2330': {
        'stock_code': '2330',
        'company_name': '台灣積體電路製造公司 (台積電)',
        'short_name': '台積電',
        'industry': '半導體業',
        'address': '台灣新竹市',
        'chairman': '劉德音',
        'founded_date': '1987-02-21',
        'listed_date': '1994-09-05',
        'par_value_per_share': 10,
        'paid_in_capital': '2,590 億元',
        'total_shares_issued': '25,900,000,000 股',
        'website': 'https://www.tsmc.com',
    },
}

# 模擬歷史股價數據
historical_data = {
    '2330': [
        {'date': '2024-09-01', 'open': 600, 'close': 610, 'high': 615, 'low': 595},
        {'date': '2024-09-02', 'open': 610, 'close': 620, 'high': 625, 'low': 605},
    ],
}

# 模擬財務分析數據
financial_data = {
    '2330': {
        'revenue': '1,500 億元',
        'netIncome': '300 億元',
        'grossMargin': 50,
        'eps': 5.2,
    },
}

# 公司詳細信息 API
@app.route('/STOCK/data_id_info', methods=['GET'])
def get_company_info():
    stock_code = request.args.get('value')
    if stock_code in company_data:
        return jsonify({'content': [company_data[stock_code]]})
    else:
        return jsonify({'error': '公司信息未找到'}), 404

# 歷史股價 API
@app.route('/historical/<stock_code>', methods=['GET'])
def get_historical_data(stock_code):
    if stock_code in historical_data:
        return jsonify(historical_data[stock_code])
    else:
        return jsonify({'error': '歷史股價數據未找到'}), 404

# 財務分析 API
@app.route('/financial/<stock_code>', methods=['GET'])
def get_financial_data(stock_code):
    if stock_code in financial_data:
        return jsonify(financial_data[stock_code])
    else:
        return jsonify({'error': '財務分析數據未找到'}), 404

# 技術分析圖表 API
@app.route('/technical_analysis/<stock_code>', methods=['GET'])
def get_technical_analysis(stock_code):
    # 檢查該 HTML 文件是否存在
    html_file = f'{stock_code}_kd_chart.html'
    if os.path.exists(html_file):
        # 使用當前目錄
        return send_from_directory(os.getcwd(), html_file)
    else:
        return jsonify({'error': '技術分析圖表未找到'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
