from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import requests

def get_FinancialAnalysisIndex_year(year, sii):
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

    # 獲取當前的年份
    current_year = datetime.now().year

    # 確認今年的資料是否完整
    if check_data_completeness(current_year, sii_id_df):
        # 獲取上市公司的資料
        df_sii = get_FinancialAnalysisIndex_year(current_year, 'sii')
    else:
        # 若今年資料不完整，則使用前一年的資料
        previous_year = current_year - 1
        df_sii = get_FinancialAnalysisIndex_year(previous_year, 'sii')

    # 替換 '-' 和 '*****' 還有 'NA' 為 '無'
    df_sii.replace({'-': '無', '*****': '無', 'NA': '無'}, inplace=True)

    # 儲存上市公司的資料到 CSV 檔案中
    sii_csv_file_name = "sii_stock_financial_analysis.csv"
    df_sii.to_csv(f'./stock_financial_analysis/{sii_csv_file_name}', index=False, encoding='utf-8-sig')

    print(f"上市公司資料已儲存到 ./stock_financial_analysis/{sii_csv_file_name}")

def check_data_completeness(year, sii_df):
    # 檢查上市公司股票代碼是否存在於當年的資料中
    sii_ids = sii_df['股票代碼'].tolist()

    df_sii = get_FinancialAnalysisIndex_year(year, 'sii')

    # 檢查上市公司的股票代碼
    sii_data_ids = df_sii['股票代碼'].unique().tolist()
    for sii_id in sii_ids:
        if sii_id not in sii_data_ids:
            return False
    
    return True

def extract_and_save_selected_data(input_csv):
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

    # 將提取的列儲存回原來的 CSV 檔案
    df_selected.to_csv(input_csv, index=False, encoding='utf-8-sig')

    print(f"選擇的上市公司資料已儲存到 {input_csv}")

# 呼叫主函數
if __name__ == "__main__":
    main()

# 呼叫函數，處理上市公司的財務分析資料
input_csv = './stock_financial_analysis/sii_stock_financial_analysis.csv'
extract_and_save_selected_data(input_csv)

# 設定指定股票代碼檔案的路徑
stock_codes_path = r'C:\Users\yingh\Desktop\python爬蟲\50股.xlsx'

# 讀取指定股票代碼
stock_codes_df = pd.read_excel(stock_codes_path)
stock_codes = stock_codes_df['股票代碼'].tolist()  # 假設股票代碼欄位名稱為 "股票代碼"

# 設定要讀取的 CSV 檔案路徑
csv_file_path = './stock_financial_analysis/sii_stock_financial_analysis.csv'

# 從已存的 CSV 中讀取資料
filtered_df = pd.read_csv(csv_file_path)

# 篩選出符合指定股票代碼的資料
filtered_df = filtered_df[filtered_df['股票代碼'].isin(stock_codes)]

# 設定篩選後的 CSV 檔案路徑
filtered_csv_path = './stock_financial_analysis/sii_stock_financial_analysis_filtered.csv'

# 將篩選後的資料寫入新的 CSV 檔案
filtered_df.to_csv(filtered_csv_path, index=False, encoding='utf-8-sig')

print(f'篩選後的資料已成功儲存到 {filtered_csv_path}')