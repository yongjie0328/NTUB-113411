from datetime import datetime, timedelta
import requests as r
import pandas as pd

def fetch_data_for_date(date):
    url = f'https://www.twse.com.tw/rwd/zh/fund/T86?date={date}&selectType=ALLBUT0999&response=json&_={date}'
    res = r.get(url)
    if res.ok:
        try:
            inv_json = res.json()
            return inv_json
        except ValueError:
            return None
    return None

def get_data_for_past_days(days):
    today = datetime.now()
    all_data = []
    
    for i in range(days):
        date_str = today.strftime('%Y%m%d')
        inv_json = fetch_data_for_date(date_str)
        if inv_json and 'data' in inv_json and inv_json['data']:
            print(f"成功獲取日期 {date_str} 的數據。")
            data = inv_json['data']
            fields = inv_json['fields']
            df = pd.DataFrame(data, columns=fields)
            df['日期'] = date_str  
            all_data.append(df)
        else:
            print(f"日期 {date_str} 沒有數據或無法獲取。")
        today -= timedelta(days=1)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        # 重新排序列，使 '日期' 列位於最前面
        cols = ['日期'] + [col for col in combined_df.columns if col != '日期']
        combined_df = combined_df[cols]
        return combined_df
    return None

# 獲取過去 30 天的數據
days = 30
combined_df = get_data_for_past_days(days)
if combined_df is not None:
    # 儲存合併後的 DataFrame 到 CSV 檔案
    filename = f"./stock_institutional_investors/sii_stock_institutional_investors.csv"
    combined_df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f'過去30天的資料已儲存到 ./stock_institutional_investors/sii_stock_institutional_investors.csv 檔案中。')

    # 讀取 CSV 文件
    df = pd.read_csv(filename)

    # 打印原始列名
    print("原始列名:", df.columns)

    # 確保 DataFrame 中的 '證券代號' 欄位存在
    if '證券代號' in df.columns:
        # 更改列名
        df.rename(columns={'證券代號': '股票代碼'}, inplace=True)
        
        # 儲存修改後的 DataFrame 到 CSV 檔案
        new_filename = f"./stock_institutional_investors/sii_stock_institutional_investors.csv"
        df.to_csv(new_filename, index=False, encoding='utf-8-sig')
        print(f'已成功將證券代號更名為股票代碼，並成功存到 ./stock_institutional_investors/sii_stock_institutional_investors.csv 檔案中。')

    # 讀取上市股票代碼檔案
    sii_stock_id_df = pd.read_csv("./stock_price/sii_stock_id.csv")

    # 確保數據為字符串類型並去除空白字符
    sii_stock_id_df['股票代碼'] = sii_stock_id_df['股票代碼'].astype(str).str.strip()
    df['股票代碼'] = df['股票代碼'].astype(str).str.strip()

    # 確保 DataFrame 中的 '股票代碼' 欄位存在
    if '股票代碼' in sii_stock_id_df.columns:
        # 找出在 df 中但不在 sii_stock_id_df 中的股票代碼
        tdr_data = df[~df['股票代碼'].isin(sii_stock_id_df['股票代碼'])]['股票代碼'].tolist()
        print("在 df 中但不在 sii_stock_id_df 中的股票代碼：", tdr_data)
        
        # 從 df 中刪除不在 sii_stock_id_df 中的股票代碼
        df_filtered = df[df['股票代碼'].isin(sii_stock_id_df['股票代碼'])]
        
        # 儲存修改後的 DataFrame 到檔案中
        filtered_filename = f"./stock_institutional_investors/sii_stock_institutional_investors.csv"
        df_filtered.to_csv(filtered_filename, index=False, encoding='utf-8-sig')
        print(f"已成功從 df 中刪除不在 sii_stock_id_df 中的股票代碼，並成功存回 ./stock_institutional_investors/sii_stock_institutional_investors.csv 檔案中。")
    else:
        print("sii_stock_id_df 中找不到 '股票代碼' 欄位")
else:
    print(f"未能獲取過去 {days} 天的數據。")