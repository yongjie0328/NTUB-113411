from datetime import datetime, timedelta
import requests as r
import pandas as pd
import random
import time

# 證交所個股日成交資訊
def get_tw_stock_data(start_year, start_month, end_year, end_month, stock_code):
    start_date = str(datetime(start_year, start_month, 1).strftime('%Y-%m-%d'))
    end_date = str(datetime(end_year, end_month, 1).strftime('%Y-%m-%d'))
    month_list = pd.date_range(start_date, end_date, freq='MS').strftime("%Y%m%d").tolist()

    df = pd.DataFrame()
    for month in month_list:
        url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="+ month + "&stockNo=" + str(stock_code)
        res = r.get(url)
        stock_json = res.json()
        stock_df = pd.DataFrame.from_dict(stock_json['data'])
        df = pd.concat([df, stock_df], ignore_index=True)

    # 資料轉型
    for col in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        for row in range(df.shape[0]):
            # 把"日期"從字串(string)換成時間(datetime)，並將民國年換成西元年
            if col == 0:
                day = df.iloc[row,0].split('/')
                df.iloc[row, 0] = datetime(int(day[0]) + 1911, int(day[1]), int(day[2])).strftime('%Y-%m-%d')  
    
    df.columns = ['日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數']
    return df

# 讀取 sii_stock_info_select.csv 檔案並提取上市股票代碼
df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_info\sii_stock_info_select.csv", usecols=['股票代碼'])
df.to_csv('./stock_price/sii_stock_id.csv', index=False, encoding='utf-8-sig')
print("股票代碼已儲存到 './stock_price/sii_stock_id.csv' 檔案中。")

# 股票代碼欄位名稱為'股票代碼'
stock_code_list = df['股票代碼'].tolist()

# 前30日個股歷史價格
def get_multi_tw_stock_data(stock_code_list):
    df = pd.DataFrame()
    no_data_list = []  # 存放沒有資料的股票代碼清單
    for stock_code in stock_code_list:
        try:
            current_time = datetime.now()
            current_year = current_time.year
            current_month = current_time.month

            thirty_days_ago = current_time - timedelta(days=30)
            start_year = thirty_days_ago.year
            start_month = thirty_days_ago.month
        
            stock_df = get_tw_stock_data(stock_code=stock_code, start_year=start_year, start_month=start_month, end_year=current_year, end_month=current_month)
            stock_df.insert(0, '股票代碼', stock_code)
            df = pd.concat([df, stock_df], ignore_index=True)
        except Exception as e:
            print(f"找不到股票代碼 {stock_code} 的資料：{e}")
            no_data_list.append(stock_code)
            continue
        time.sleep(random.uniform(2, 5))
    print("沒有資料的股票代碼清單：", no_data_list)
    return df , no_data_list 

# 獲取單日的股票資料
def get_tw_stock_data_day(stock_code, day):
    url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={day}&stockNo={stock_code}"
    res = r.get(url)
    if res.status_code == 200:
        stock_json = res.json()
        if 'data' in stock_json:
            stock_df = pd.DataFrame.from_dict(stock_json['data'])
            stock_df.columns = ['日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數']
            stock_df['日期'] = stock_df['日期'].apply(lambda x: datetime.strptime(f"{int(x.split('/')[0])+1911}/{x.split('/')[1]}/{x.split('/')[2]}", '%Y/%m/%d').strftime('%Y-%m-%d'))
            return stock_df
    return None

# 前30日個股歷史價格
def get_multi_tw_stock_data_day(no_data_list):
    df2 = pd.DataFrame()

    # 針對 no_data_list 裡面的股票代碼，逐天爬取價格資料
    for stock_code in no_data_list:
        try:
            current_time = datetime.now()
            for i in range(30):
                day = (current_time - timedelta(days=i)).strftime('%Y%m%d')
                stock_df = get_tw_stock_data_day(stock_code, day)
                if stock_df is not None:
                    stock_df.insert(0, '股票代碼', stock_code)
                    df2 = pd.concat([df, stock_df], ignore_index=True)
                    print(f"獲取到股票代碼 {stock_code} 在 {day} 的資料。")
                else:
                    print(f"找不到股票代碼 {stock_code} 在 {day} 的資料。")
                time.sleep(random.uniform(2, 5))
        except Exception as e:
            print(f"針對股票代碼 {stock_code} 的逐天資料爬取失敗：{e}")
            continue

    return df2

# 執行多股股票資料獲取
df, no_data_list = get_multi_tw_stock_data(stock_code_list)
df2 = get_multi_tw_stock_data_day(no_data_list)

# 合併資料框
combined_df = pd.concat([df, df2], ignore_index=True)

combined_df.to_csv('./stock_price/sii_stock_price.csv', index=False, encoding='utf-8-sig')
print("股票歷史價格資料已儲存到 './stock_price/sii_stock_price.csv' 檔案中。")

# 讀取 sii_stock_price.csv 檔案
df = pd.read_csv('./stock_price/sii_stock_price.csv')

# 獲取今天日期
end_date = datetime.now().strftime('%Y-%m-%d')

# 計算前30天的日期
start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

# 選取日期範圍
selected_data = df[(df['日期'] >= start_date) & (df['日期'] <= end_date)]

# 印出所選日期範圍的資料
print(selected_data)

# 將所選日期範圍的資料儲存到另一個 CSV 檔案中
selected_data.to_csv('./stock_price/sii_stock_price_select.csv', index=False, encoding='utf-8-sig')
print("所選日期範圍的資料已儲存到 './stock_price/sii_stock_price_select.csv' 檔案中。")