import plotly.graph_objects as go
import pandas as pd
import os

# 讀取 CSV 檔案
csv_filename = 'stock_technical_analysis/sii_stock_technical_analysis.csv'
df = pd.read_csv(csv_filename)

# 獲取所有唯一的股票代碼
tickers = df['Ticker'].unique()

# 確保目標資料夾存在
output_dir = './stock_technical_analysis/stock_technical_analysis_image/'
os.makedirs(output_dir, exist_ok=True)  # 如果資料夾不存在則創建

# 繪製各個技術指標的圖表
for ticker in tickers:
    ticker_data = df[df['Ticker'] == ticker]

    # 1. 成交量圖
    fig_volume = go.Figure()
    fig_volume.add_trace(go.Bar(x=ticker_data.index, y=ticker_data['Volume'], name='成交量', marker_color='lightblue'))
    fig_volume.update_layout(title=f'{ticker} 成交量圖', xaxis_title='日期', yaxis_title='成交量', template='plotly_white')
    fig_volume.show()
    # 保存成交量圖為動態HTML
    fig_volume.write_html(f'{output_dir}{ticker}_volume_chart.html')

    # 2. 移動平均線 (MA) 圖
    fig_ma = go.Figure()
    fig_ma.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['Close'], mode='lines', name='收盤價', line=dict(color='blue')))
    fig_ma.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['MA20'], mode='lines', name='MA20', line=dict(color='orange')))
    fig_ma.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['MA50'], mode='lines', name='MA50', line=dict(color='green')))
    fig_ma.update_layout(title=f'{ticker} 移動平均線 (MA) 圖', xaxis_title='日期', yaxis_title='價格', template='plotly_white')
    fig_ma.show()
    # 保存移動平均線圖為動態HTML
    fig_ma.write_html(f'{output_dir}{ticker}_ma_chart.html')

    # 3. MACD 圖
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['MACD'], mode='lines', name='MACD', line=dict(color='purple')))
    fig_macd.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['Signal Line'], mode='lines', name='信號線', line=dict(color='red')))
    fig_macd.update_layout(title=f'{ticker} MACD 圖', xaxis_title='日期', yaxis_title='MACD', template='plotly_white')
    fig_macd.show()
    # 保存MACD圖為動態HTML
    fig_macd.write_html(f'{output_dir}{ticker}_macd_chart.html')

    # 4. RSI 圖
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['RSI'], mode='lines', name='RSI', line=dict(color='brown')))
    fig_rsi.update_layout(title=f'{ticker} RSI 圖', xaxis_title='日期', yaxis_title='RSI', template='plotly_white')
    fig_rsi.show()
    # 保存RSI圖為動態HTML
    fig_rsi.write_html(f'{output_dir}{ticker}_rsi_chart.html')

    # 5. KD指標圖
    fig_kd = go.Figure()
    fig_kd.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['K'], mode='lines', name='K 值', line=dict(color='pink')))
    fig_kd.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['D'], mode='lines', name='D 值', line=dict(color='lightgreen')))
    fig_kd.update_layout(title=f'{ticker} KD 指標圖', xaxis_title='日期', yaxis_title='KD 值', template='plotly_white')
    fig_kd.show()
    # 保存KD指標圖為動態HTML
    fig_kd.write_html(f'{output_dir}{ticker}_kd_chart.html')