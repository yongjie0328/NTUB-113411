import plotly.graph_objects as go
import yfinance as yf
import pandas as pd

# 下載台積電的股價數據 (台積電代碼: 2330.TW)
tsmc = yf.Ticker("2330.TW")
data = tsmc.history(start="2024-01-01", end="2024-06-30")

# 檢查是否存在數據
if data.empty:
    print("數據未下載成功，請檢查網絡連接或日期範圍。")
else:
    # 計算 RSV、K、D 值
    n = 9  # 通常 n 為 9 天
    data['Lowest_9'] = data['Low'].rolling(window=n).min()
    data['Highest_9'] = data['High'].rolling(window=n).max()
    
    # 計算 RSV
    data['RSV'] = (data['Close'] - data['Lowest_9']) / (data['Highest_9'] - data['Lowest_9']) * 100

    # 初始化 K 和 D 值為浮點數類型
    data['K'] = 50.0  # K 值初始為 50.0
    data['D'] = 50.0  # D 值初始為 50.0

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

    # 添加圖表標題、軸標籤以及範圍選擇按鈕
    fig.update_layout(
        title='台積電 2024 年 1 月到 6 月的 KD 指標圖',
        xaxis_title='日期',
        yaxis_title='KD 值',
        hovermode='x',
        template='plotly_white',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1個月", step="month", stepmode="backward"),
                    dict(count=3, label="3個月", step="month", stepmode="backward"),
                    dict(count=6, label="6個月", step="month", stepmode="backward"),
                    dict(step="all", label="全部")
                ])
            ),
            rangeslider=dict(visible=False),  # 禁用下方的範圍滑桿
            type="date"
        )
    )

    # 顯示互動式圖表
    fig.show()
