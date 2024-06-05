from datetime import datetime, date
import matplotlib.dates as mdates
import matplotlib.pyplot as plt 
from bs4 import BeautifulSoup
import requests as r
import pandas as pd

# 櫃買中心每5秒指數盤後統計
# 請求網頁內容
url = "https://www.tpex.org.tw/web/stock/iNdex_info/minute_index/1MIN.php?l=zh-tw"
res = r.get(url)
res.encoding = 'utf-8-sig'
html_content = res.text

# 解析 HTML
soup = BeautifulSoup(html_content, "html.parser")

# 找到表格標題列所在的標籤
thead = soup.find("thead")

# 找到標題列中的每一個標題
titles = []
for th in thead.find_all("th"):
    titles.append(th.text.strip())

# 定義函數以獲取每日股票資料
def get_stock_daily(year, month, day):
    while True:
        # 構建日期字串，格式為 "YYYYMMDD"
        search_date = str(date(year, month, day).strftime("%Y%m%d"))

        # 提取年份、月份和日期
        year_str = search_date[:4]
        month_str = search_date[4:6]
        day_str = search_date[6:8]

        # 將年份轉換為民國年
        roc_year = str(int(year_str) - 1911)

        # 組合成 "yyy/mm/dd" 格式
        formatted_date = f"{roc_year}/{month_str}/{day_str}"

        # 設置請求URL
        url = f"https://www.tpex.org.tw/web/stock/iNdex_info/minute_index/1MIN_result.php?l=zh-tw&d=" + formatted_date

        # 發送請求獲取資料
        res = r.get(url)
        stock_json = res.json()

        # 初始化資料集
        df = pd.DataFrame()

        # 檢查今天有無資料
        if 'aaData' in stock_json:
            stock_df = pd.DataFrame(stock_json['aaData'])
            if stock_df.empty:  # 檢查 DataFrame 是否為空
                print(f"No data available for {formatted_date}. Retrieving data for the previous day.")
                # 如果今天無資料，則抓取前一天的資料
                day -= 1
                continue
            stock_df.columns = titles
            df = pd.concat([df, stock_df], ignore_index=True)
            search_date = date(year, month, day)
            return df, search_date
        else:
            print(f"No data available for {formatted_date}. Retrieving data for the previous day.")
            # 如果今天無資料，則抓取前一天的資料
            day -= 1

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
    
    # 排除時間為 "99:99:99" 的資料
    daily_stock = daily_stock[daily_stock["時 間"] != "99:99:99"]

    # 儲存股票資料為 CSV 檔案
    daily_stock.to_csv("./stock_index/otc_stock_index.csv", index=False, encoding='utf-8-sig')

    print(f"上櫃公司資料已儲存為 ./stock_index/otc_stock_index.csv 檔案")

    # 選擇需要的列
    columns_to_keep = ['時 間', '紡纖纖維', '電機機械', '鋼鐵工業', '建材營造', '航運業', '觀光餐旅', '其他', 
                   '化學工業', '生技醫療', '半導體業', '電腦週邊業', '光電業', '通信網路業', '電子零組件業', 
                   '電子通路業', '資訊服務業', '其他電子業', '文化創意業', '綠能環保', '數位雲端', '居家生活', 
                   '電子工業', '櫃買指數', '成交金額(萬元)', '成交張數', '成交筆數', '委買筆數', '委賣筆數', 
                   '委買張數', '委賣張數']
	  	 							 	 	 					
    daily_stock = daily_stock[columns_to_keep]

    # 移除股票指數中的逗號並轉換為浮點數
    for col in daily_stock.columns[1:]:
        daily_stock[col] = daily_stock[col].str.replace(',', '').astype(float)

    # 將時間列轉換為日期時間格式
    daily_stock["時 間"] = pd.to_datetime(daily_stock["時 間"])

    # 生成每個指數的折線圖並儲存為圖片檔案
    for col in daily_stock.columns[1:]:
        fig, ax = plt.subplots(figsize=(20, 5))
        
        ax.plot(daily_stock["時 間"], daily_stock[col], color="blue")
        ax.grid(axis='both')
        
    # 設定 x 軸顯示的時間格式為幾點幾分
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.title(f"{search_date.year}-{search_date.month}-{search_date.day} {col}")
        plt.xlabel("時間")
        plt.ylabel('價格')

        image_path = f"./stock_index/otc_stock_index_image/{col}.png"
        fig.savefig(image_path, facecolor='white')
        plt.close(fig)