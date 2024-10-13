from datetime import datetime, timedelta
import requests as r
import pandas as pd
import random
import time

# 獲取股票資料（逐月或逐日）
def get_tw_stock_data(stock_code, start_date, end_date, freq='M'):
    date_range = pd.date_range(start_date, end_date, freq=freq).strftime("%Y%m%d").tolist()
    df = pd.DataFrame()

    for date in date_range:
        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stock_code}"
        res = r.get(url)
        if res.status_code == 200:
            stock_json = res.json()
            if 'data' in stock_json:
                stock_df = pd.DataFrame(stock_json['data'], columns=[
                    '日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數'
                ])
                # 轉換日期格式
                stock_df['日期'] = stock_df['日期'].apply(
                    lambda x: datetime.strptime(f"{int(x.split('/')[0]) + 1911}/{x.split('/')[1]}/{x.split('/')[2]}", '%Y/%m/%d').strftime('%Y-%m-%d'))
                stock_df.insert(0, '股票代碼', stock_code)
                df = pd.concat([df, stock_df], ignore_index=True)
        else:
            print(f"找不到股票代碼 {stock_code} 在 {date} 的資料。")
        time.sleep(random.uniform(2, 5))  # 可根据实际情况减少或移除

    return df

# 批量獲取股票資料
def get_multi_tw_stock_data(stock_code_list, start_date, end_date):
    df = pd.DataFrame()
    no_data_list = []  # 存放沒有資料的股票代碼清單

    for stock_code in stock_code_list:
        try:
            stock_df = get_tw_stock_data(stock_code, start_date, end_date)
            if not stock_df.empty:
                df = pd.concat([df, stock_df], ignore_index=True)
            else:
                no_data_list.append(stock_code)
        except Exception as e:
            print(f"找不到股票代碼 {stock_code} 的資料：{e}")
            no_data_list.append(stock_code)

    return df, no_data_list

# 主執行程序
if __name__ == "__main__":
    # 讀取股票代碼
    df_codes = pd.read_excel(r"C:\Users\yingh\Desktop\python爬蟲\50股.xlsx", usecols=['股票代碼'])
    stock_code_list = df_codes['股票代碼'].tolist()

    # 計算前30天的日期範圍
    current_date = datetime.now().strftime('%Y-%m-%d')
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    # 獲取前30日個股歷史價格
    df, no_data_list = get_multi_tw_stock_data(stock_code_list, thirty_days_ago, current_date)

    # 若有股票代碼無法獲取，針對這些股票逐日獲取數據
    if no_data_list:
        df2, _ = get_multi_tw_stock_data(no_data_list, thirty_days_ago, current_date, freq='D')
        df = pd.concat([df, df2], ignore_index=True)

    # 儲存結果
    df.to_csv('./stock_price/sii_stock_price_filtered.csv', index=False, encoding='utf-8-sig')
    print("所選日期範圍的資料已儲存到 './stock_price/sii_stock_price_filtered.csv' 檔案中。")