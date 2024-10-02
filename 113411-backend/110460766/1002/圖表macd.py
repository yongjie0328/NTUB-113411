import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd

# 下載台積電的股價數據 (台積電代碼: 2330.TW)
tsmc = yf.Ticker("2330.TW")
data = tsmc.history(start="2024-01-01", end="2024-06-30")

# 計算短期 EMA（12天）
data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()

# 計算長期 EMA（26天）
data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()

# 計算 MACD 線
data['MACD'] = data['EMA12'] - data['EMA26']

# 計算信號線（9天的 MACD 線的 EMA）
data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

# 計算 MACD 柱狀圖
data['Histogram'] = data['MACD'] - data['Signal']

# 找到 MACD 和信號線的交叉點
cross_up = []  # 金叉
cross_down = []  # 死叉

for i in range(1, len(data)):
    if data['MACD'].iat[i-1] < data['Signal'].iat[i-1] and data['MACD'].iat[i] > data['Signal'].iat[i]:
        cross_up.append((data.index[i], data['MACD'].iat[i]))  # 記錄金叉
    elif data['MACD'].iat[i-1] > data['Signal'].iat[i-1] and data['MACD'].iat[i] < data['Signal'].iat[i]:
        cross_down.append((data.index[i], data['MACD'].iat[i]))  # 記錄死叉

# 使用 Plotly 繪製互動式圖表
fig = go.Figure()

# 添加 MACD 線
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['MACD'],
    mode='lines',
    name='MACD',
    line=dict(color='orange'),
    hovertemplate='日期: %{x}<br>MACD: %{y:.2f}<extra></extra>'
))

# 添加信號線
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Signal'],
    mode='lines',
    name='Signal',
    line=dict(color='purple'),
    hovertemplate='日期: %{x}<br>信號線: %{y:.2f}<extra></extra>'
))

# 繪製 MACD 柱狀圖
histogram_positive = data[data['Histogram'] >= 0]
histogram_negative = data[data['Histogram'] < 0]

fig.add_trace(go.Bar(
    x=histogram_positive.index,
    y=histogram_positive['Histogram'],
    name='Positive Histogram',
    marker=dict(color='red'),
    hovertemplate='日期: %{x}<br>柱狀圖: %{y:.2f}<extra></extra>'
))

fig.add_trace(go.Bar(
    x=histogram_negative.index,
    y=histogram_negative['Histogram'],
    name='Negative Histogram',
    marker=dict(color='green'),
    hovertemplate='日期: %{x}<br>柱狀圖: %{y:.2f}<extra></extra>'
))

# 標記金叉和死叉點
if cross_up:
    fig.add_trace(go.Scatter(
        x=[p[0] for p in cross_up],
        y=[p[1] for p in cross_up],
        mode='markers',
        name='金叉 (MACD 上穿 Signal)',
        marker=dict(color='red', size=10, symbol='triangle-up'),
        hovertemplate='金叉<br>日期: %{x}<br>MACD: %{y:.2f}<extra></extra>'
    ))

if cross_down:
    fig.add_trace(go.Scatter(
        x=[p[0] for p in cross_down],
        y=[p[1] for p in cross_down],
        mode='markers',
        name='死叉 (MACD 下穿 Signal)',
        marker=dict(color='green', size=10, symbol='triangle-down'),
        hovertemplate='死叉<br>日期: %{x}<br>MACD: %{y:.2f}<extra></extra>'
    ))

# 設置圖表標題和軸標籤
fig.update_layout(
    title='台積電 2024 年 1 月到 6 月的 MACD 指標圖',
    xaxis_title='日期',
    yaxis_title='數值',
    hovermode='x unified',
    template='plotly_white',
    dragmode='zoom',  # 設置為縮放模式
    xaxis=dict(
        rangeslider=dict(visible=True),  # 啟用下方的範圍滑桿
        type='date'
    )
)


# 啟用滾輪縮放功能
fig.update_xaxes(fixedrange=False)
fig.update_yaxes(fixedrange=False)


# 保存為 HTML 文件
html_file = 'tsmc_macd_chart.html'
fig.write_html(html_file, config={'scrollZoom': True})

# 創建一個 PyQt5 應用程序
app = QApplication(sys.argv)

# 創建一個主窗口
window = QMainWindow()
window.setWindowTitle('台積電 2024 年 MACD 指標圖')
window.setGeometry(100, 100, 1200, 800)  # 設定窗口大小

# 創建一個 QWebEngineView 小部件來顯示 HTML
view = QWebEngineView()
view.load(QUrl.fromLocalFile(os.path.abspath(html_file)))

# 將 QWebEngineView 添加到主窗口
window.setCentralWidget(view)

# 顯示窗口
window.show()

# 運行應用程序
sys.exit(app.exec_())
