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
data = tsmc.history(start="2023-01-01", end="2023-12-31")

# 計算30日移動平均線
data['30_MA'] = data['Close'].rolling(window=30).mean()

# 去除 NaN 值
data.dropna(inplace=True)

# 使用 Plotly 繪製互動式圖表
fig = go.Figure()

# 添加收盤價線圖
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Close'],
    mode='lines',
    name='收盤價',
    line=dict(color='blue'),
    hovertemplate='日期: %{x}<br>收盤價: %{y:.2f}<extra></extra>'
))

# 添加30日移動平均線圖
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['30_MA'],
    mode='lines',
    name='30日移動平均線',
    line=dict(color='red'),
    hovertemplate='日期: %{x}<br>30日移動平均線: %{y:.2f}<extra></extra>'
))

# 設置圖表標題、軸標籤以及範圍選擇按鈕
fig.update_layout(
    title='台積電 2023 年股價與 30 日移動平均線',
    xaxis_title='日期',
    yaxis_title='價格 (台幣)',
    hovermode='x',
    template='plotly_white',
    dragmode='pan',  # 設置為平移模式
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1個月", step="month", stepmode="backward"),
                dict(count=3, label="3個月", step="month", stepmode="backward"),
                dict(count=6, label="6個月", step="month", stepmode="backward"),
                dict(step="all", label="全部")
            ])
        ),
        rangeslider=dict(visible=True),  # 啟用下方的範圍滑桿
        type="date"
    )
)

# 啟用滾輪縮放功能
fig.update_xaxes(fixedrange=False)
fig.update_yaxes(fixedrange=False)

# 保存為 HTML 文件
html_file = 'tsmc_ma_chart.html'
fig.write_html(html_file, config={'scrollZoom': True})

# 創建一個 PyQt5 應用程序
app = QApplication(sys.argv)

# 創建一個主窗口
window = QMainWindow()
window.setWindowTitle('台積電 2023 年股價與 30 日移動平均線')
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
