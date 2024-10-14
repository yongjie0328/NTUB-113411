import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 下載台積電的股價數據 (台積電代碼: 2330.TW)
tsmc = yf.Ticker("2330.TW")
data = tsmc.history(start="2024-01-01", end="2024-06-30")

# 計算漲跌幅
data['Change'] = data['Close'].diff()

# 計算漲跌幅中漲幅（正值）和跌幅（負值）
data['Gain'] = data['Change'].where(data['Change'] > 0, 0)
data['Loss'] = -data['Change'].where(data['Change'] < 0, 0)

# 計算平均漲幅和平均跌幅（14 天）
n = 14
data['Avg_Gain'] = data['Gain'].rolling(window=n, min_periods=1).mean()
data['Avg_Loss'] = data['Loss'].rolling(window=n, min_periods=1).mean()

# 計算相對強度（RS）
data['RS'] = data['Avg_Gain'] / data['Avg_Loss']

# 計算 RSI 指標
data['RSI'] = 100 - (100 / (1 + data['RS']))

# 使用 Plotly 繪製互動式圖表
fig = go.Figure()

# 添加 RSI 線圖
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['RSI'],
    mode='lines',
    name='RSI',
    line=dict(color='blue'),
    hovertemplate='日期: %{x}<br>RSI: %{y:.2f}<extra></extra>'
))

# 繪製超買和超賣水平線
fig.add_trace(go.Scatter(
    x=data.index,
    y=[70] * len(data.index),
    mode='lines',
    name='超買區 (70)',
    line=dict(color='red', dash='dash'),
    hovertemplate='超買區 (70)<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=data.index,
    y=[30] * len(data.index),
    mode='lines',
    name='超賣區 (30)',
    line=dict(color='green', dash='dash'),
    hovertemplate='超賣區 (30)<extra></extra>'
))

# 設置圖表標題、軸標籤以及範圍選擇按鈕
fig.update_layout(
    title='台積電 2024 年 1 月到 6 月的 RSI 指標圖',
    xaxis_title='日期',
    yaxis_title='RSI 值',
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
html_file = 'tsmc_rsi_chart.html'
fig.write_html(html_file, config={'scrollZoom': True})

# 創建一個 PyQt5 應用程序
app = QApplication(sys.argv)

# 創建一個主窗口
window = QMainWindow()
window.setWindowTitle('台積電 RSI 指標圖')
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
