import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# 讀取csv文件
df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_price\sii_stock_price_filtered.csv")

# 讀取50股.xlsx文件中的公司簡稱
stock_info = pd.read_excel(r"C:\Users\yingh\Desktop\python爬蟲\50股.xlsx")

# 合併股票數據和公司簡稱
df = pd.merge(df, stock_info[['股票代碼', '公司簡稱']], on='股票代碼', how='left')

# 解析日期列，自動推斷格式
df['日期'] = pd.to_datetime(df['日期'])

# 設定日期範圍為過去30天
end_date = pd.to_datetime('today')  # 當前日期
start_date = end_date - pd.DateOffset(days=30)  # 30天前的日期

# 篩選日期範圍內的資料
df_filtered = df[(df['日期'] >= start_date) & (df['日期'] <= end_date)]

# 確保有資料
if not df_filtered.empty:
    # 獲取所有股票代號
    stock_codes = df_filtered["股票代碼"].unique()

    # 設定中文字體
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 使用微軟雅黑體字型替代

    # 為每個股票代號繪圖
    for stock_code in stock_codes:
        df_stock = df_filtered[df_filtered["股票代碼"] == stock_code]

        # 獲取該股票代碼的股票名稱
        stock_name = df_stock["公司簡稱"].iloc[0] if "公司簡稱" in df_stock.columns else "未知名稱"

        # 如果有時間列，按時間排序
        if '時間' in df_stock.columns:
            df_stock = df_stock.sort_values(by="時間")

        # 使用 '時間' 列，否則使用 '日期' 列
        time = df_stock["時間"] if '時間' in df_stock.columns else df_stock["日期"]
        high_price = df_stock["最高價"]
        low_price = df_stock["最低價"]
        end_price = df_stock["收盤價"]

        plt.figure(figsize=(14, 8))  # 調整圖表大小
        plt.plot(time, high_price, color="red", alpha=0.7, label="最高價", linewidth=2.5)  # 紅色標示最高價
        plt.plot(time, low_price, color="green", linewidth=2.5, alpha=0.8, label="最低價")  # 綠色標示最低價
        plt.plot(time, end_price, color="blue", linestyle="dashed", label="收盤價", marker='o', markersize=6, linewidth=2.5)  # 藍色標示收盤價

        # 設置日期格式化和旋轉角度
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=30, ha='right', fontstyle='italic')  # 設置日期旋轉30度且斜體

        plt.xlabel("時間", fontsize=12)
        plt.ylabel("價格", fontsize=12)

        # 将图例放置在图表外部
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=12, frameon=False)  # 調整圖例位置和樣式
        
        # 標題包含股票代碼和名稱
        plt.title(f"{stock_code} {stock_name} 在 {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 的價格走勢圖", fontsize=16)

        # 調整網格線顏色和樣式
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')  # 調淡網格線

        # 調整圖表邊距
        plt.subplots_adjust(left=0.1, right=0.75, top=0.9, bottom=0.2)  # 調整右邊距，以便有足夠空間顯示圖例

        # 存成圖片
        plt.savefig(f"./stock_price/sii_stock_price_image/{stock_code}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}_chart.png")  # 存放在指定目錄
        plt.close()  # 關閉當前圖表，避免重疊
else:
    print(f"日期範圍 {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 沒有數據或數據格式有誤。")
