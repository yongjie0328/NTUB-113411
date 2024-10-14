import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from matplotlib import font_manager

# 設定 matplotlib 支援中文
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 可改為 'SimHei'（黑體）或其他支援中文的字體
plt.rcParams['axes.unicode_minus'] = False  # 解決座標軸負號顯示問題

# 設定股票代碼（台灣 0050 ETF）
target_stock = '0050.TW'
csv_file_path = './data/0050.csv'

# 檢查是否已存在 CSV 檔案，如果不存在則下載資料
if not os.path.exists(csv_file_path):
    # 使用 yfinance 下載歷史資料
    df = yf.download(target_stock, start='2020-01-01', end='2023-01-01')
    
    # 檢查下載到的資料
    if not df.empty:
        # 創建資料夾
        os.makedirs('./data', exist_ok=True)
        
        # 將資料儲存為 CSV 檔案
        df.to_csv(csv_file_path)
        print(f'股票資料已成功儲存為 {csv_file_path}')
    else:
        print('無法下載股票資料，請檢查股票代碼和網路連線。')
else:
    # 從現有 CSV 檔案讀取資料
    df = pd.read_csv(csv_file_path, parse_dates=True, index_col=0)
    print(f'已從 {csv_file_path} 讀取股票資料。')

# 檢查資料是否存在
if not df.empty:
    # 定義市場顏色和樣式
    mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)

    # 設定繪圖參數
    kwargs = dict(type='candle', mav=(5, 20, 60), volume=True, figratio=(10, 8), figscale=0.75, title=target_stock, style=s)

    # 創建互動式圖表
    fig, axes = mpf.plot(df, **kwargs, returnfig=True)

    # 添加注釋框
    annot = axes[0].annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                             bbox=dict(boxstyle="round", fc="w"),
                             arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    # 定義更新注釋框的函數
    def update_annot(x):
        # 取得日期和股價資訊
        date = df.index[x]
        row = df.iloc[x]
        text = (f"日期: {date.strftime('%Y-%m-%d')}\n"
                f"開盤: {row['Open']:.2f}\n"
                f"收盤: {row['Close']:.2f}\n"
                f"最高: {row['High']:.2f}\n"
                f"最低: {row['Low']:.2f}")
        annot.set_text(text)
        annot.xy = (x, row['Close'])
        annot.get_bbox_patch().set_alpha(0.9)

    # 定義滑鼠移動事件
    def on_hover(event):
        if event.inaxes == axes[0]:
            # 獲取鼠標的 x 座標
            x = int(event.xdata)
            if x >= 0 and x < len(df):
                update_annot(x)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                annot.set_visible(False)
                fig.canvas.draw_idle()

    # 綁定滑鼠移動事件
    fig.canvas.mpl_connect("motion_notify_event", on_hover)

    # 顯示互動式圖表
    plt.show()
else:
    print('無法繪製圖表，因為沒有有效的股票資料。')