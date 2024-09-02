from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np

# 設置字體，這裡使用本地字體文件路徑
font_path = r"C:\Windows\Fonts\msyh.ttc"  # 假設使用 Microsoft YaHei 字體
my_font = FontProperties(fname=font_path)

# 從 CSV 檔案中讀取股票代碼和股票名稱
sii_stock_info = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_info\sii_stock_info_select.csv", usecols=['股票代碼', '公司簡稱'], dtype=str)
otc_stock_info = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_info\otc_stock_info_select.csv", usecols=['股票代碼', '公司簡稱'], dtype=str)

# 合併上市股票和上櫃股票代碼與名稱
stock_info = pd.concat([sii_stock_info, otc_stock_info]).drop_duplicates().reset_index(drop=True)

# 添加 .TW 以符合台灣市場的股票代碼
stock_info['股票代碼'] = stock_info['股票代碼'] + '.TW'

# 設置時間範圍，抓取120天前的數據 #數據設30天的話K線會因為資料量不足而導致圖表只有一個點
end = dt.date.today()  
start = end - dt.timedelta(days=120)  

def calculate(df, indicator):
    if indicator == "8日MA與13日MA":
        df['8_MA'] = df['Close'].rolling(window=8).mean()
        df['13_MA'] = df['Close'].rolling(window=13).mean()
    elif indicator == "EMA和MACD":
        df['EMA'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['MACD'] = df['Close'].ewm(span=26, adjust=False).mean() - df['Close'].ewm(span=12, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD'].ewm(span=9, adjust=False).mean()
    elif indicator == "RSI":
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
    elif indicator == "月K線":
        df = df.set_index('Date')
        df = df.resample('ME').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
        df = df.reset_index()
    return df

def plot_stock(df, stock_id, stock_name, indicators=[], filename=None):
    df = df.set_index('Date')
    
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index)

    num = 10
    if len(df) < num:
        num = len(df)
    date = df.index.strftime('%Y-%m-%d')
    
    if len(indicators) > 0:
        fig, ax = plt.subplots(len(indicators) + 1, 1, figsize=(12, 8), sharex=True)
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
    
    title = f'{stock_name} ({stock_id})'
    
    if isinstance(ax, np.ndarray):
        ax[0].plot(df['Close'], label='Close')
        ax[0].set_title(title, fontproperties=my_font)
        ax[0].set_ylabel('Price', color='blue', rotation=0, ha='right', fontproperties=my_font)
        ax[0].set_xticks(df.index[::len(df)//num])
        ax[0].set_xticklabels(date[::len(df)//num], rotation=45, fontproperties=my_font)
        
        for i, indicator in enumerate(indicators, start=1):
            if indicator == 'Volume':
                ax[i].bar(df.index, df['Volume'], color='green')
                ax[i].set_ylabel('Volume', color='green', rotation=0, ha='right', fontproperties=my_font)
            elif indicator == 'MACD_Histogram':
                if 'MACD_Histogram' in df.columns:
                    ax[i].bar(df.index, df['MACD_Histogram'], alpha=0.5, color='red')
                    ax[i].set_ylabel('MACD', color='red', rotation=0, ha='right', fontproperties=my_font)
    else:
        ax.plot(df['Close'], label='Close')
        ax.set_title(title, fontproperties=my_font)
        ax.set_ylabel('Price', color='blue', rotation=0, ha='right', fontproperties=my_font)
        ax.set_xticks(df.index[::len(df)//num])
        ax.set_xticklabels(date[::len(df)//num], rotation=45, fontproperties=my_font)

    plt.tight_layout()

    if filename:
        plt.savefig(filename)
        print(f"圖表已保存為 {filename}")

    plt.close()  # 關閉圖表窗口

def process_stock(stock_id, stock_name):
    try:
        df = yf.download(stock_id, start=start, end=end).reset_index()

        if df.empty:
            print(f"警告: 股票 {stock_id} ({stock_name}) 的數據為空或無法下載。")
            failed_stocks.append(stock_id)
            return

        df_ma = calculate(df, "8日MA與13日MA")
        plot_stock(df_ma, stock_id, stock_name, indicators=['Volume'], filename=f'./stock_technical_analysis/MA_IMAGES/{stock_id}_8_MA_13_MA_Volume.png')

        df_macd = calculate(df, "EMA和MACD")
        plot_stock(df_macd, stock_id, stock_name, indicators=['MACD_Histogram'], filename=f'./stock_technical_analysis/MACD_IMAGES/{stock_id}_EMA_MACD_Histogram.png')

        df_rsi = calculate(df, "RSI")
        plot_stock(df_rsi, stock_id, stock_name, indicators=[], filename=f'./stock_technical_analysis/RSI_IMAGES/{stock_id}_RSI.png')

        df_monthly = calculate(df, "月K線")
        plot_stock(df_monthly, stock_id, stock_name, indicators=[], filename=f'./stock_technical_analysis/KLine_IMAGES/{stock_id}_Monthly_K_Line.png')

    except Exception as e:
        print(f"處理股票 {stock_id} ({stock_name}) 時出現錯誤: {e}")
        failed_stocks.append(stock_id)

# 記錄下載失敗的股票代碼
failed_stocks = []

# 處理所有股票代碼
for _, row in stock_info.iterrows():
    process_stock(row['股票代碼'], row['公司簡稱'])

print("無法下載的股票代碼:", failed_stocks)