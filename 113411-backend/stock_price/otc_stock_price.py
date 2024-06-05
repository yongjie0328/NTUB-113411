from datetime import datetime, timedelta
import requests as r
import pandas as pd
import random
import time

#櫃買中心個股日成交資訊
def get_tw_stock_data(month_list, stock_code):
    df = pd.DataFrame()
    for month in month_list:
        url = "https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?l=zh-tw&d=" + month + "&stkno="+ str(stock_code)
        res = r.get(url)
        stock_json = res.json()
        
        if 'aaData' in stock_json:
            stock_df = pd.DataFrame(stock_json['aaData'], columns=['日期', '成交仟股', '成交仟元', '開盤', '最高', '最低', '收盤', '漲跌', '筆數'])
            df = pd.concat([df, stock_df], ignore_index=True)
        else:
            print(f"No data found for {month}")

    if len(df) == 0:
        print("No data available for the specified period.")
    return df

# 讀取 otc_stock_info_select.csv 檔案並提取上櫃股票代碼
df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_info\otc_stock_info_select.csv", usecols=['股票代碼'])
df.to_csv('./stock_price/otc_stock_id.csv', index=False, encoding='utf-8-sig')
print("股票代碼已儲存到 'otc_stock_id.csv' 檔案中。")

# 股票代碼欄位名稱為 '股票代碼'
stock_code_list = df['股票代碼'].tolist()

def get_multi_tw_stock_data(stock_code_list):
    df = pd.DataFrame()
    no_data_list = []  # 存放沒有資料的股票代碼清單
    for stock_code in stock_code_list:
        try:
            current_time = datetime.now()    
            current_year = current_time.year - 1911  # 轉換為民國年
            current_month = current_time.month
            thirty_days_ago = current_time - timedelta(days=30)
            start_year = thirty_days_ago.year - 1911  # 轉換為民國年
            start_month = thirty_days_ago.month

            month_list = [f"{start_year}/{start_month:02d}", f"{current_year}/{current_month:02d}"]

            stock_df = get_tw_stock_data(start_year=start_year, start_month=start_month, current_year=current_year, current_month=current_month, month_list=month_list, stock_code=stock_code)  # 將 month_list 傳遞給函式
            if len(stock_df) == 0:
                no_data_list.append(stock_code)
            else:
                stock_df.insert(0, '股票代碼', stock_code)
                df = pd.concat([df, stock_df], ignore_index=True)
        except Exception as e:
            print(f"找不到股票代碼 {stock_code} 的資料：{e}")
            continue
        time.sleep(random.uniform(2, 5))
    print("沒有資料的股票代碼清單：", no_data_list)
    return df


df = get_multi_tw_stock_data(stock_code_list)
df.to_csv('./stock_price/otc_stock_price.csv', index=False, encoding='utf-8-sig')
print("股票代碼已儲存到 'otc_stock_price.csv' 檔案中。")

# 讀取 otc_stock_price.csv 檔案
df = pd.read_csv('./stock_price/otc_stock_price.csv')

# 獲取今天日期
current_date = datetime.now()

# 將西元年轉為民國年
roc_year = current_date.year - 1911

# 格式化日期為民國年月日格式
roc_date = current_date.strftime(f"{roc_year}/%m/%d")

# 計算前30天的日期
thirty_days_ago = current_date - timedelta(days=30)
roc_thirty_days_ago = thirty_days_ago.strftime(f"{roc_year}/%m/%d")

# 建立空的 DataFrame 存放符合條件的搜索結果
query_data = pd.DataFrame(columns=df.columns)

# 逐行檢查 DataFrame
for index, row in df.iterrows():
    if row['日期'] <= roc_date and row['日期'] >= roc_thirty_days_ago:
        query_data = pd.concat([query_data, pd.DataFrame([row])])
print(query_data)

# 將所選日期範圍的資料儲存到另一個 CSV 檔案中
query_data.to_csv('./stock_price/otc_stock_price_select.csv', index=False, encoding='utf-8-sig')
print("所選日期範圍的資料已儲存到 './stock_price/otc_stock_price_select.csv' 檔案中。")