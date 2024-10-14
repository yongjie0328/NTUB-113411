#內建版
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

# 檢查是否存在數據
if not data.empty:
    # 計算 RSV、K、D 值
    n = 9
    data['Lowest_9'] = data['Low'].rolling(window=n).min()
    data['Highest_9'] = data['High'].rolling(window=n).max()
    
    # 計算 RSV
    data['RSV'] = (data['Close'] - data['Lowest_9']) / (data['Highest_9'] - data['Lowest_9']) * 100

    # 初始化 K 和 D 值為浮點數類型
    data['K'] = 50.0
    data['D'] = 50.0

    # 計算 K 和 D 值
    for i in range(1, len(data)):
        if pd.notna(data['RSV'].iat[i]):
            data['K'].iat[i] = 2/3 * data['K'].iat[i-1] + 1/3 * data['RSV'].iat[i]
            data['D'].iat[i] = 2/3 * data['D'].iat[i-1] + 1/3 * data['K'].iat[i]

    # 去除 NaN 值
    data.dropna(inplace=True)

    # 使用 Plotly 繪製互動式 KD 圖表
    fig = go.Figure()

    # 添加 K 值折線圖
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['K'], 
        mode='lines', 
        name='K值', 
        line=dict(color='red'),
        hovertemplate='日期: %{x}<br>K值: %{y:.2f}<extra></extra>'
    ))

    # 添加 D 值折線圖
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['D'], 
        mode='lines', 
        name='D值', 
        line=dict(color='blue'),
        hovertemplate='日期: %{x}<br>D值: %{y:.2f}<extra></extra>'
    ))

    # 設置圖表標題、軸標籤以及範圍選擇按鈕
    fig.update_layout(
        title='台積電 2024 年 1 月到 6 月的 KD 指標圖',
        xaxis_title='日期',
        yaxis_title='KD 值',
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
    html_file = 'tsmc_kd_chart.html'
    fig.write_html(html_file, config={'scrollZoom': True})

    # 創建一個 PyQt5 應用程序
    app = QApplication(sys.argv)

    # 創建一個主窗口
    window = QMainWindow()
    window.setWindowTitle('台積電 KD 指標圖')
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
