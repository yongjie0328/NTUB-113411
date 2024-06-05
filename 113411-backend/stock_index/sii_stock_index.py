from datetime import datetime, date, timedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt 
import requests as r
import pandas as pd

# 證交所每5秒指數盤後統計
# 定義函數以獲取每日股票資料
def get_stock_daily(year, month, day):
    # 初始化資料集
    df = pd.DataFrame()

    # 開始往前搜索資料
    search_date = date(year, month, day)

    while True:
        # 構建日期字串
        stock_date = str(search_date.strftime("%Y%m%d"))

        # 設置請求URL
        url = f"https://www.twse.com.tw/exchangeReport/MI_5MINS_INDEX?response=json&date={stock_date}"

        # 發送請求獲取資料
        res = r.get(url)
        stock_json = res.json()

        if 'data' in stock_json:
            # 若有資料則處理並返回
            stock_df = pd.DataFrame(stock_json['data'])
            stock_df.columns = stock_json['fields']
            df = pd.concat([df, stock_df], ignore_index=True)
            return df, search_date
        else:
            print(f"No data available for {stock_date}, searching for previous day.")
            # 若無資料則往前一天搜索
            search_date -= timedelta(days=1)

# 獲取今天的日期
today = datetime.now()
year = today.year
month = today.month
day = today.day

# 獲取股票資料
daily_stock, search_date = get_stock_daily(year, month, day)

if daily_stock is not None:    
    print("daily_stock row counts:", daily_stock.shape[0], "\ndaily_stock column counts:", daily_stock.shape[1]) # 查看總共有幾列資料跟幾個欄位
    print(daily_stock)

    # 儲存股票資料為 CSV 檔案
    daily_stock.to_csv("./stock_index/sii_stock_index.csv", index=False, encoding='utf-8-sig')

    print(f"上市公司資料已儲存為 ./stock_index/sii_stock_index.csv 檔案")

    # 選擇需要的列
    columns_to_keep = ['時間', '發行量加權股價指數', '未含金融保險股指數', '未含電子股指數', '未含金融電子股指數', 
                       '水泥類指數', '食品類指數', '塑膠類指數', '紡織纖維類指數', '電機機械類指數', '電器電纜類指數',
                       '化學生技醫療類指數', '化學類指數', '生技醫療類指數', '玻璃陶瓷類指數', '造紙類指數', '鋼鐵類指數', 
                       '橡膠類指數', '汽車類指數', '電子類指數', '半導體類指數', '電腦及週邊設備類指數', '光電類指數', 
                       '通信網路類指數', '電子零組件類指數', '電子通路類指數', '資訊服務類指數', '其他電子類指數', 
                       '建材營造類指數', '航運類指數', '觀光餐旅類指數', '金融保險類指數', '貿易百貨類指數', '油電燃氣類指數', 
                       '綠能環保類指數', '數位雲端類指數', '運動休閒類指數', '居家生活類指數', '其他類指數']
    
    daily_stock = daily_stock[columns_to_keep]

    # 移除股票指數中的逗號並轉換為浮點數
    for col in daily_stock.columns[1:]:
        daily_stock[col] = daily_stock[col].str.replace(',', '').astype(float)

    # 將時間列轉換為日期時間格式
    daily_stock["時間"] = pd.to_datetime(daily_stock["時間"])

    # 生成每個指數的折線圖並儲存為圖片檔案
    for col in daily_stock.columns[1:]:
        fig, ax = plt.subplots(figsize=(20, 5))
        
        ax.plot(daily_stock["時間"], daily_stock[col], color="blue")
        ax.grid(axis='both')
        
        # 設定 x 軸顯示的時間格式為幾點幾分
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.title(f"{search_date.year}-{search_date.month}-{search_date.day} {col}")
        plt.xlabel("時間")
        plt.ylabel('價格')

        image_path = f"./stock_index/sii_stock_index_image/{col}.png"
        fig.savefig(image_path, facecolor='white')
        plt.close(fig)