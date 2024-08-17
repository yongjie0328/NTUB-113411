from IPython.display import display, clear_output
from urllib.request import urlopen
import pandas as pd
import datetime
import sched
import time
import json

s = sched.scheduler(time.time, time.sleep)

# 定義 DataFrame 以儲存上櫃股票的資料
otc_data = pd.DataFrame()

def tableColor(val):
    if val > 0:
        color = 'red'
    elif val < 0:
        color = 'green'
    else:
        color = 'white'
    return 'color: %s' % color

def stock_crawler(targets, index=0, market_type='otc'):
    global otc_data
    clear_output(wait=True)
    
    if index >= len(targets):
        # 上櫃股票處理完畢後將資料儲存到 CSV 文件
        if market_type == 'otc':
            otc_data.to_csv('./stock_price/otc_stock_price_now.csv', index=False, encoding='utf-8-sig')
            print("上櫃股票資料已儲存到 ./stock_price/otc_stock_price_now.csv")
        return
    
    stock_code = targets[index]
    
    # 組成股票清單
    stock_list = 'otc_{}.tw'.format(stock_code)
    
    # 查詢資料
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=" + stock_list
    
    try:
        response = urlopen(query_url)
        response_data = response.read().decode('utf-8')

        if not response_data:
            raise ValueError("Empty response")

        data = json.loads(response_data)
        print(data)
    except Exception as e:
        print(f"獲取股票 {stock_code} 的資料時出現錯誤: {e}")
        time.sleep(1)  # 等待1秒後重試
        s.enter(1, 0, stock_crawler, argument=(targets, index + 1, market_type))
        return

    # 選擇需要的欄位
    columns = ['c', 'n', 'z', 'tv', 'v', 'o', 'h', 'l', 'y']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['股票代號', '公司簡稱', '當盤成交價', '當盤成交量', '累積成交量', '開盤價', '最高價', '最低價', '昨收價']
    df.insert(9, "漲跌百分比", 0.0)
    
    # 新增漲跌百分比
    for x in range(len(df.index)):
        try:
            if df.loc[x, '當盤成交價'] != '-':
                df.loc[x, ['當盤成交價', '當盤成交量', '累積成交量', '開盤價', '最高價', '最低價', '昨收價']] = df.loc[x, ['當盤成交價', '當盤成交量', '累積成交量', '開盤價', '最高價', '最低價', '昨收價']].astype(float)
                df.loc[x, '漲跌百分比'] = (df.loc[x, '當盤成交價'] - df.loc[x, '昨收價']) / df.loc[x, '昨收價'] * 100
        except ValueError as e:
            print(f"跳過股票 {df.loc[x, '股票代號']} 由於數據缺失或無效。")
            continue
    
    # 將當前股票的資料新增到 DataFrame 中
    otc_data = pd.concat([otc_data, df], ignore_index=True)
    
    # 記錄更新時間
    time_now = datetime.datetime.now()
    print("更新時間: " + str(time_now.hour) + ":" + str(time_now.minute))
    
    # 顯示表格
    df = df.style.apply(tableColor, subset=['漲跌百分比'])
    display(df)
    
    # 設置下一次爬取時間
    s.enter(1, 0, stock_crawler, argument=(targets, index + 1, market_type))

# 讀取上櫃股票代碼的 CSV 文件
otc_stock_id = pd.read_csv('./stock_price/otc_stock_id.csv')

# 提取股票代碼列，列名為 '股票代碼'
otc_stock_list = otc_stock_id['股票代碼'].tolist()

# 每秒定時器
s.enter(1, 0, stock_crawler, argument=(otc_stock_list, 0, 'otc'))
s.run()