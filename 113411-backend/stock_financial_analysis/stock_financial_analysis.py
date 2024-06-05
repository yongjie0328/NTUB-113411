from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import requests

def get_FinancialAnalysisIndex_year(year, sii_or_otc):
    # 將年份轉換為民國年份格式
    roc_year = year - 1911

    # 預設表單資料
    form_data = {
        'encodeURIComponent': 1,
        'step': 1,
        'firstin': 1,
        'off': 1,
        'TYPEK': 'sii',  # 'sii' 為上市
        'year': roc_year,
    }

    if sii_or_otc.lower() == 'otc':
        form_data['TYPEK'] = 'otc' # 'otc' 為上櫃 

    # 從網站獲取資料
    data = get_data_from_mops_twse('https://mops.twse.com.tw/mops/web/t51sb02', form_data)

    # 從提取的資料創建 DataFrame
    df = pd.DataFrame(np.array(data), columns=[
        '股票代碼', '公司簡稱', '財務結構-負債佔資產比率(%)', '財務結構-長期資金佔不動產、廠房及設備比率(%)', 
        '償債能力-流動比率(%)', '償債能力-速動比率(%)', '償債能力-利息保障倍數(%)', '經營能力-應收款項週轉率(次)', 
        '經營能力-平均收現日數', '經營能力-存貨週轉率(次)', '經營能力-平均售貨日數', '經營能力-不動產、廠房及設備週轉率(次)', 
        '經營能力-總資產週轉率(次)', '獲利能力-資產報酬率(%)', '獲利能力-權益報酬率(%)', '獲利能力-稅前純益佔實收資本比率(%)', 
        '獲利能力-純益率(%)', '獲利能力-每股盈餘(元)', '現金流量-現金流量比率(%)', '現金流量-現金流量允當比率(%)', 
        '現金流量-現金再投資比率(%)'
    ])

    return df

def get_data_from_mops_twse(url, form_data):
    # 發送 POST 請求
    response = requests.post(url, data=form_data)
    response.encoding = 'utf8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有具有 class "hasBorder" 的表格
    tables = soup.find_all("table", {"class": "hasBorder"})

    data = []
    for tb in tables:
        for row in tb.find_all("tr"):
            tempdata = []
            for col in row.find_all('td'):
                col.attrs = {}
                tempdata.append(col.text.strip().replace('\u3000', ''))
            if len(tempdata) > 1:  # 避免添加無用資料的行
                data.append(tempdata)
    
    return data

def main():
    # 讀取上市公司的股票代碼
    sii_id_df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_price\sii_stock_id.csv")

    # 讀取上櫃公司的股票代碼
    otc_id_df = pd.read_csv(r"C:\Users\yingh\Desktop\python爬蟲\stock_price\otc_stock_id.csv")

    # 獲取當前的年份
    current_year = datetime.now().year

    # 確認今年的資料是否完整
    if check_data_completeness(current_year, sii_id_df, otc_id_df):
        # 獲取上市公司的資料
        df_sii = get_FinancialAnalysisIndex_year(current_year, 'sii')
        
        # 獲取上櫃公司的資料
        df_otc = get_FinancialAnalysisIndex_year(current_year, 'otc')

    else:
        # 若今年資料不完整，則使用前一年的資料
        previous_year = current_year - 1
        df_sii = get_FinancialAnalysisIndex_year(previous_year, 'sii')
        df_otc = get_FinancialAnalysisIndex_year(previous_year, 'otc')

    # 替換 '-' 和 '*****' 還有 'NA' 為 '無'
    df_sii.replace({'-': '無', '*****': '無', 'NA': '無'}, inplace=True)
    df_otc.replace({'-': '無', '*****': '無', 'NA': '無'}, inplace=True)

    # 分別儲存上市和上櫃公司的資料到 CSV 檔案中
    sii_csv_file_name = "sii_stock_financial_analysis.csv"
    otc_csv_file_name = "otc_stock_financial_analysis.csv"

    df_sii.to_csv(f'./stock_financial_analysis/{sii_csv_file_name}', index=False, encoding='utf-8-sig')
    df_otc.to_csv(f'./stock_financial_analysis/{otc_csv_file_name}', index=False, encoding='utf-8-sig')

    print(f"上市公司資料已儲存到 ./stock_financial_analysis/{sii_csv_file_name}")
    print(f"上櫃公司資料已儲存到 ./stock_financial_analysis/{otc_csv_file_name}")
    
    # 合併兩個 DataFrame
    df_combined = pd.concat([df_sii, df_otc], ignore_index=True)

    # 將合併後的 DataFrame 儲存到 CSV 檔案中
    csv_file_name = "stock_financial_analysis.csv"
    
    df_combined.to_csv(f'./stock_financial_analysis/{csv_file_name}', index=False, encoding='utf-8-sig')

    print(f"上市跟上櫃資料已儲存到 ./stock_financial_analysis/{csv_file_name}")

def check_data_completeness(year, sii_df, otc_df):
    # 檢查上市公司和上櫃公司的股票代碼是否都存在於當年的資料中
    sii_ids = sii_df['股票代碼'].tolist()
    otc_ids = otc_df['股票代碼'].tolist()

    df_sii = get_FinancialAnalysisIndex_year(year, 'sii')
    df_otc = get_FinancialAnalysisIndex_year(year, 'otc')

    # 檢查上市公司的股票代碼
    sii_data_ids = df_sii['股票代碼'].unique().tolist()
    for sii_id in sii_ids:
        if sii_id not in sii_data_ids:
            return False
    
    # 檢查上櫃公司的股票代碼
    otc_data_ids = df_otc['股票代碼'].unique().tolist()
    for otc_id in otc_ids:
        if otc_id not in otc_data_ids:
            return False
    
    return True

def extract_and_save_selected_data(input_csv, output_csv):

    # 讀取已合併的 CSV 檔案
    df = pd.read_csv(input_csv)

    # 選擇需要的列
    selected_columns = [
        '股票代碼', '公司簡稱', '償債能力-流動比率(%)', '償債能力-速動比率(%)', '償債能力-利息保障倍數(%)', 
        '經營能力-應收款項週轉率(次)', '經營能力-平均收現日數', '經營能力-存貨週轉率(次)', '經營能力-平均售貨日數',
        '經營能力-不動產、廠房及設備週轉率(次)', '經營能力-總資產週轉率(次)', '獲利能力-資產報酬率(%)',
        '獲利能力-權益報酬率(%)', '獲利能力-稅前純益佔實收資本比率(%)', '獲利能力-純益率(%)', '獲利能力-每股盈餘(元)'
    ]

    # 提取選擇的列
    df_selected = df[selected_columns]

    # 將提取的列儲存到新的 CSV 檔案中
    df_selected.to_csv(output_csv, index=False, encoding='utf-8-sig')

    print(f"選擇的上市跟上櫃資料已儲存到 {output_csv}")

# 調用主函數
if __name__ == "__main__":
    main()

# 調用函數
input_csv = './stock_financial_analysis/stock_financial_analysis.csv'
output_csv = './stock_financial_analysis/stock_financial_analysis_select.csv'
extract_and_save_selected_data(input_csv, output_csv)

# 讀取股票代碼跟股票財務分析檔案
stock_id_df = pd.read_csv("./stock_revenue/stock_id.csv")
stock_financial_analysis_select_df = pd.read_csv("./stock_financial_analysis/stock_financial_analysis_select.csv")

# 找出在 stock_financial_analysis_select 中但不在 stock_id 中的股票代碼，這些資料為存託憑證
tdr_data = stock_financial_analysis_select_df[~stock_financial_analysis_select_df['股票代碼'].isin(stock_id_df['股票代碼'])]['股票代碼'].tolist()
print("在 stock_financial_analysis_select_df 中但不在 stock_id 中的股票代碼：", tdr_data)

# 從 stock_financial_analysis_select DataFrame 中刪除在 stock_id 中不存在的股票代碼
stock_financial_analysis_select_df = stock_financial_analysis_select_df[~stock_financial_analysis_select_df['股票代碼'].isin(tdr_data)]

# 儲存修改後的 stock_revenue DataFrame 到檔案中
stock_financial_analysis_select_df.to_csv("./stock_financial_analysis/stock_financial_analysis_select.csv", index=False, encoding='utf-8-sig')
print("已成功從 stock_financial_analysis_select 中刪除在 stock_id 中不存在的股票代碼，並成功存回 ./stock_financial_analysis/stock_financial_analysis_select.csv 檔案中。")

# 找出在 stock_id 中但不在 stock_financial_analysis_select 中的股票代碼，這些資料為沒財務分析的股票代碼
no_financial_analysis_data = stock_id_df[~stock_id_df['股票代碼'].isin(stock_financial_analysis_select_df['股票代碼'])]['股票代碼'].tolist()
print("在 stock_id 中但不在 stock_financial_analysis_select 中的股票代碼：", no_financial_analysis_data)

# 先確定要新增的行數
num_new_rows = len(no_financial_analysis_data)

# 為每個欄位填入 '無'
new_rows = pd.DataFrame({
    column: ['無'] * num_new_rows
    for column in stock_financial_analysis_select_df.columns
})

# 填寫股票代碼
new_rows['股票代碼'] = no_financial_analysis_data

# 將資料新增到 stock_financial_analysis_select_df
updated_stock_financial_analysis_select_df = pd.concat([stock_financial_analysis_select_df, new_rows], ignore_index=True)

# 將更新後的 DataFrame 存回 CSV 檔案
updated_stock_financial_analysis_select_df.to_csv('./stock_financial_analysis/stock_financial_analysis_select.csv', index=False, encoding='utf-8-sig')

print("更新後的資料已成功存回 './stock_financial_analysis/stock_financial_analysis_select.csv' 檔案中。")