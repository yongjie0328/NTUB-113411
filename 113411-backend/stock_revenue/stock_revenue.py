from datetime import datetime
import pandas as pd
import requests
import locale

# 在爬取股票資料的函數中進行判斷並打印訊息
def crawl_stock_data(url, stock_code):
    res = requests.get(url)
    res.encoding = 'big5'
    if res.status_code == 200:
        html_df = pd.read_html(res.text)           

        # 去除行數錯誤的表格，並合併表格
        df = pd.concat([df for df in html_df if df.shape[1] == 11]) 
        print(df)

        # 如果 DataFrame 為空，則打印無資料訊息
        if df.empty:
            print(f"股票代碼 {stock_code} 無營收資料。")
        else:
            # 設置表頭
            df.columns = df.columns.get_level_values(1)

            # 去除多餘列, 重新排序索引
            df = df[df['公司名稱'] != '合計']
            df = df.reset_index(drop=True) 

        return df
    else:
        print(f"當前月份 股票代碼 {stock_code} 無營收資料。")
        return None

# 定義儲存資料的函數
def save_stock_data(df, filename):
    # 將特定欄位格式化
    df['當月營收'] = df['當月營收'].apply(lambda x: '{:,.0f}'.format(x))
    df['上月營收'] = df['上月營收'].apply(lambda x: '{:,.0f}'.format(x))
    df['去年當月營收'] = df['去年當月營收'].apply(lambda x: '{:,.0f}'.format(x))
    df['當月累計營收'] = df['當月累計營收'].apply(lambda x: '{:,.0f}'.format(x))
    df['去年累計營收'] = df['去年累計營收'].apply(lambda x: '{:,.0f}'.format(x))
    df['上月比較 增減(%)'] = df['上月比較 增減(%)'].apply(lambda x: '{:.2f}'.format(x))
    df['去年同月 增減(%)'] = df['去年同月 增減(%)'].apply(lambda x: '{:.2f}'.format(x))
    df['前期比較 增減(%)'] = df['前期比較 增減(%)'].apply(lambda x: '{:.2f}'.format(x))
    
    # 修改列名
    df.rename(columns={
        '公司 代號': '股票代碼',
        '公司名稱': '公司簡稱',
        '當月營收': '當月營收(千元)',
        '上月營收': '上月營收(千元)',
        '去年當月營收': '去年當月營收(千元)',
        '當月累計營收': '當月累計營收(千元)',
        '去年累計營收': '去年累計營收(千元)',
        '上月比較 增減(%)': '上月比較增減(%)',
        '去年同月 增減(%)': '去年同月增減(%)',
        '前期比較 增減(%)': '前期比較增減(%)',
    }, inplace=True)
    
    # 替換 '-' 和 'nan' 為 '無'
    df.replace({'-': '無', 'nan': '無'}, inplace=True)

    # 將 DataFrame 儲存為 CSV 檔案
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"資料已成功儲存到 '{filename}' 檔案中。")

def process(urls):
    all_successful = True  # 初始化為 True，表示所有操作都成功
    for category, url in urls.items():
        df = crawl_stock_data(url, category)
        if df is not None:
            filename = f"./stock_revenue/{category}_stock_revenue.csv"
            save_stock_data(df, filename)
        else:
            all_successful = False
    
    return all_successful
        
def concate():
    # 讀取四個 CSV 檔案並合併成一個 DataFrame
    tw_sii_df = pd.read_csv("./stock_revenue/tw_sii_stock_revenue.csv")
    int_sii_df = pd.read_csv("./stock_revenue/int_sii_stock_revenue.csv")
    tw_otc_df = pd.read_csv("./stock_revenue/tw_otc_stock_revenue.csv")
    int_otc_df = pd.read_csv("./stock_revenue/int_otc_stock_revenue.csv")

    # 將四個 DataFrame 合併成一個
    combined_df = pd.concat([tw_sii_df, int_sii_df, tw_otc_df, int_otc_df])

    # 儲存合併後的 DataFrame 為一個新的 CSV 檔案
    combined_df.to_csv("./stock_revenue/stock_revenue.csv", index=False, encoding='utf-8-sig')
    print("四個 CSV 檔案已成功合併並儲存為 './stock_revenue/stock_revenue.csv' 檔案。")

if __name__ == '__main__':
    # 讀取上市股票代碼檔案
    sii_df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_price\sii_stock_id.csv")

    # 讀取上櫃股票代碼檔案
    otc_df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_price\otc_stock_id.csv")

    # 合併上市與上櫃股票代碼資料
    combined_df = pd.concat([sii_df, otc_df])

    # 儲存合併後的 DataFrame 為一個新的 CSV 檔案
    combined_df.to_csv("./stock_revenue/stock_id.csv", index=False, encoding='utf-8-sig')
    print("上市與上櫃股票代碼已成功合併並儲存為 './stock_revenue/stock_id.csv' 檔案。")

    # 設置以使用千分位分隔符號
    locale.setlocale(locale.LC_NUMERIC, '')

    # 獲取當前日期的年份和月份
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    # 如果當前月份為1月份，則上個月為去年的12月份；否則上個月為當前年份的前一個月份
    if current_month == 1:
        last_month_year = current_year - 1 - 1911  # 西元年轉民國年
        last_month = 12
    else:
        last_month_year = current_year - 1911  # 西元年轉民國年
        last_month = current_month - 1

    # 格式化日期的年份與月份
    last_month_date = f"{last_month_year}_{last_month}"
    current_month_date = f"{current_year}_{current_month}"

    # 爬取股票資料並儲存到對應的檔案中
    date = current_month_date # 先預設這個月的url
    stock_urls = {
        'tw_sii': f'https://mops.twse.com.tw/nas/t21/sii/t21sc03_{date}_0.html', #國內上市股票
        'int_sii': f'https://mops.twse.com.tw/nas/t21/sii/t21sc03_{date}_1.html', #國外上市股票
        'tw_otc': f'https://mops.twse.com.tw/nas/t21/otc/t21sc03_{date}_0.html', #國內上櫃股票
        'int_otc': f'https://mops.twse.com.tw/nas/t21/otc/t21sc03_{date}_1.html' #國外上櫃股票
    }

    success = process(stock_urls) # 判斷是否有獲取到資料並存檔
    if success:
        concate()
        # print("資料已成功儲存到 './stock_revenue/stock_revenue.csv' 檔案中。")
    else:
        previous_date = last_month_date
        last_month_stock_urls = {
            'tw_sii': f'https://mops.twse.com.tw/nas/t21/sii/t21sc03_{previous_date}_0.html', #國內上市股票
            'int_sii': f'https://mops.twse.com.tw/nas/t21/sii/t21sc03_{previous_date}_1.html', #國外上市股票
            'tw_otc': f'https://mops.twse.com.tw/nas/t21/otc/t21sc03_{previous_date}_0.html', #國內上櫃股票
            'int_otc': f'https://mops.twse.com.tw/nas/t21/otc/t21sc03_{previous_date}_1.html' #國外上櫃股票
        }
        success_2nd = process(last_month_stock_urls) # 判斷"上個月"是否有獲取到資料並存檔
        if success_2nd:
            concate()
            # print("資料已成功儲存到 './stock_revenue/stock_revenue.csv' 檔案中。")

# 讀取上市公司基本資料
sii_info_df = pd.read_csv("./stock_info/sii_stock_info_select.csv")

# 讀取上櫃公司基本資料
otc_info_df = pd.read_csv("./stock_info/otc_stock_info_select.csv")

# 合併兩個 DataFrame，只選擇 '股票代碼' 和 '公司簡稱' 列
combined_info_df = pd.concat([
    sii_info_df[['股票代碼', '公司簡稱']],
    otc_info_df[['股票代碼', '公司簡稱']]
], ignore_index=True)

# 確保 '股票代碼' 和 '公司簡稱' 是字串格式，並移除前後空格
combined_info_df['股票代碼'] = combined_info_df['股票代碼'].astype(str).str.strip()
combined_info_df['公司簡稱'] = combined_info_df['公司簡稱'].astype(str).str.strip()

# 查找這些股票
company_ids = ['2353', '2432', '3046', '6285', '6776', '6174', '6690', '6811', '8077', '8111', '8349']

# 創建一個字典來儲存股票代碼和公司簡稱的對應關係
company_names = {}

# 遍歷 company_ids 列表並獲取每個股票代碼對應的公司簡稱
for company_id in company_ids:
    try:
        company_name = combined_info_df.loc[combined_info_df['股票代碼'] == company_id, '公司簡稱'].values[0]
        company_names[company_id] = company_name
    except IndexError:
        company_names[company_id] = "沒有找到公司簡稱"

# 打印結果
for company_id, company_name in company_names.items():
    print(f"股票代碼為 {company_id} 的公司簡稱為: {company_name}")

# 讀取股票代碼跟股票營收檔案
stock_id_df = pd.read_csv("./stock_revenue/stock_id.csv")
stock_revenue_df = pd.read_csv("./stock_revenue/stock_revenue.csv")

# 使用之前創建的 company_names 字典將相應股票代碼的公司簡稱替換為正確的公司簡稱，以解決原本是亂碼的問題
for company_id, company_name in company_names.items():
    stock_revenue_df.loc[stock_revenue_df['股票代碼'] == int(company_id), '公司簡稱'] = company_name

# 儲存更新後的資料並存回 stock_revenue.csv 檔案中
stock_revenue_df.to_csv("./stock_revenue/stock_revenue.csv", index=False, encoding='utf-8-sig')
print("修改公司簡稱後的資料已成功存回 './stock_revenue/stock_revenue.csv' 檔案中。")

# 找出在 stock_revenue 中但不在 stock_id 中的股票代碼，這些資料為存託憑證
tdr_data = stock_revenue_df[~stock_revenue_df['股票代碼'].isin(stock_id_df['股票代碼'])]['股票代碼'].tolist()
print("在 stock_revenue 中但不在 stock_id 中的股票代碼：", tdr_data)

# 從 stock_revenue DataFrame 中刪除在 stock_id 中不存在的股票代碼
stock_revenue_df = stock_revenue_df[~stock_revenue_df['股票代碼'].isin(tdr_data)]

# 儲存修改後的 stock_revenue DataFrame 到檔案中
stock_revenue_df.to_csv("./stock_revenue/stock_revenue.csv", index=False, encoding='utf-8-sig')
print("已成功從 stock_revenue 中刪除在 stock_id 中不存在的股票代碼，並成功存回 './stock_revenue/stock_revenue.csv' 檔案中。")

# # 找出在 stock_id 中但不在 stock_revenue 中的股票代碼，這些資料為沒營收的股票代碼
# no_revenue_data = stock_id_df[~stock_id_df['股票代碼'].isin(stock_revenue_df['股票代碼'])]['股票代碼'].tolist()
# print("在 stock_id 中但不在 stock_revenue 中的股票代碼：", no_revenue_data)