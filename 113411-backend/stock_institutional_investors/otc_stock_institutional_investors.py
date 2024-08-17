from datetime import datetime, timedelta
import requests as r
import pandas as pd

def fetch_data_for_date(report_date_str):
    # 確保日期格式為 "yyy/mm/dd"
    url = f'https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=EW&t=D&d={report_date_str}&_={report_date_str}'

    res = r.get(url)
    if res.ok:
        try:
            inv_json = res.json()
            return inv_json
        except ValueError:
            return None
    return None

def format_date_to_report_date(date):
    # 將西元年份轉為民國年份，並格式化為 "yyy/mm/dd"
    year = date.year - 1911
    return f"{year}/{date.strftime('%m/%d')}"

def get_data_for_past_days(days):
    today = datetime.now()
    all_data = []
    
    for _ in range(days):
        report_date_str = format_date_to_report_date(today)
        print(f"嘗試獲取日期 {report_date_str} 的數據")  
        inv_json = fetch_data_for_date(report_date_str)
        if inv_json and 'aaData' in inv_json and inv_json['aaData']:
            print(f"成功獲取日期 {report_date_str} 的數據。")
            data = inv_json['aaData']
            columns = ['代號', '名稱', '外資及陸資(不含外資自營商)-買進股數', '外資及陸資(不含外資自營商)-賣出股數',
                       '外資及陸資(不含外資自營商)-買賣超股數', '外資自營商-買進股數', '外資自營商-賣出股數', 
                       '外資自營商-買賣超股數', '外資及陸資-買進股數', '外資及陸資-賣出股數', '外資及陸資-買賣超股數', 
                       '投信-買進股數', '投信-賣出股數', '投信-買賣超股數', '自營商(自行買賣)-買進股數',
                       '自營商(自行買賣)-賣出股數', '自營商(自行買賣)-買賣超股數', '自營商(避險)-買進股數',
                       '自營商(避險)-賣出股數', '自營商(避險)-買賣超股數', '自營商-買進股數', '自營商-賣出股數',
                       '自營商-買賣超股數', '三大法人買賣超股數合計', 'null']
            df = pd.DataFrame(data, columns=columns)
            df['日期'] = report_date_str
            all_data.append(df)
        else:
            print(f"日期 {report_date_str} 沒有數據或無法獲取。")
        today -= timedelta(days=1)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        cols = ['日期'] + [col for col in combined_df.columns if col != '日期']
        combined_df = combined_df[cols]
        return combined_df
    return None

# 獲取過去 30 天的數據
days = 30
combined_df = get_data_for_past_days(days)
if combined_df is not None:
    # 儲存合併後的 DataFrame 到 CSV 檔案
    filename = f"./stock_institutional_investors/otc_stock_institutional_investors.csv"
    combined_df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f'過去30天的資料已儲存到 {filename} 檔案中。')

    # 讀取 CSV 文件
    df = pd.read_csv(filename)

    # 打印原始列名
    print("原始列名:", df.columns)

    # 確保 DataFrame 中的 '代號' 欄位存在
    if '代號' in df.columns:
        # 更改列名
        df.rename(columns={'代號': '股票代碼'}, inplace=True)
        
        # 儲存修改後的 DataFrame 到 CSV 檔案
        new_filename = f"./stock_institutional_investors/otc_stock_institutional_investors.csv"
        df.to_csv(new_filename, index=False, encoding='utf-8-sig')
        print(f'已成功將代號更名為股票代碼，並成功存到 {new_filename} 檔案中。')

    # 讀取上櫃股票代碼檔案
    otc_stock_id_df = pd.read_csv("./stock_price/otc_stock_id.csv")

    # 確保數據為字符串類型並去除空白字符
    otc_stock_id_df['股票代碼'] = otc_stock_id_df['股票代碼'].astype(str).str.strip()
    df['股票代碼'] = df['股票代碼'].astype(str).str.strip()

    # 確保 DataFrame 中的 '股票代碼' 欄位存在
    if '股票代碼' in otc_stock_id_df.columns:
        # 找出在 df 中但不在 otc_stock_id_df 中的股票代碼
        tdr_data = df[~df['股票代碼'].isin(otc_stock_id_df['股票代碼'])]['股票代碼'].tolist()
        print("在 df 中但不在 otc_stock_id_df 中的股票代碼：", tdr_data)
        
        # 從 df 中刪除不在 otc_stock_id_df 中的股票代碼
        df_filtered = df[df['股票代碼'].isin(otc_stock_id_df['股票代碼'])]
        
        # 儲存修改後的 DataFrame 到檔案中
        filtered_filename = f"./stock_institutional_investors/otc_stock_institutional_investors.csv"
        df_filtered.to_csv(filtered_filename, index=False, encoding='utf-8-sig')
        print(f"已成功從 df 中刪除不在 otc_stock_id_df 中的股票代碼，並成功存回 {filtered_filename} 檔案中。")
    else:
        print("otc_stock_id_df 中找不到 '股票代碼' 欄位")
else:
    print(f"未能獲取過去 {days} 天的數據。")