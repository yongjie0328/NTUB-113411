from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time 
import csv

# 設定瀏覽器驅動程式路徑
driver_path = r'C:\Users\yingh\Desktop\python爬蟲\chromedriver.exe'

# 初始化 Chrome 瀏覽器
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# 設定等待時間
wait = WebDriverWait(driver, 10)

# 前往網頁
driver.get("https://mops.twse.com.tw/mops/web/t51sb01")

# 市場別為上市
market_type = '上市'

try:
    # 找到市場類型下拉選單
    market_select = Select(driver.find_element(By.XPATH, "//select[@name='TYPEK']"))

    # 選擇市場類型
    market_select.select_by_visible_text(market_type)

    # 顯示資料載入中，請稍後..
    wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='code']//option")))

    # 找到產業類型下拉選單
    industry_select = Select(driver.find_element(By.XPATH, "//select[@name='code']"))

    # 選擇產業類型選項
    industry_select.select_by_index(0)  # 選擇第一個選項，空值為查詢全部產業類型

    # 點擊查詢按鈕
    search_button = driver.find_element(By.XPATH, "//input[@value=' 查詢 ']")
    search_button.click()

    # 等待查詢結果加載完成
    time.sleep(10)  # 這裡等待10秒，可以根據頁面加載速度進行調整

    # 獲取網頁的原始碼
    html_content = driver.page_source

    # 使用BeautifulSoup模組解析網頁
    soup = BeautifulSoup(html_content, 'html.parser')

    # 設定上市表頭欄位名稱
    column_names = ["股票代碼", "公司名稱", "公司簡稱", "產業類別", "外國企業註冊地國", "住址", "營利事業統一編號", "董事長", "總經理",
                    "發言人", "發言人職稱", "代理發言人", "總機電話", "成立日期", "上市日期", "普通股每股面額", "實收資本額(元)",
                    "已發行普通股數或TDR原發行股數", "私募普通股(股)", "特別股(股)", "編製財務報告類型", "普通股盈餘分派或虧損撥補頻率",
                    "普通股年度(含第4季或後半年度)現金股息及紅利決議層級", "股票過戶機構", "過戶電話", "過戶地址", "簽證會計師事務所",
                    "簽證會計師1", "簽證會計師2", "英文簡稱", "英文通訊地址", "傳真機號碼", "電子郵件信箱", "公司網址", "投資人關係聯絡人",
                    "投資人關係聯絡人職稱", "投資人關係聯絡電話", "投資人關係聯絡電子郵件", "公司網站內利害關係人專區網址"]

    # 創建一個空列表來儲存表格資料
    table_data = []

    # 找到表格的標題行
    title_row = soup.find('tr')

    # 找到包含表格的元素
    table = soup.find('table')

    # 找到所有的行
    rows = table.find_all('tr')

    # 跳過第一行，即表格的標題行，從第二行開始提取資料
    for row in rows[1:]:
        # 找到每一行中的所有列
        cols1 = row.find_all(['td'])

        # 確保列數與表格標題行的列數相同，以避免爬取非表格內容
        if len(cols1) == len(column_names):
            # 提取每一列的資料，並去除空白字符
            cols_data = [col.text.strip() for col in cols1]
            
            # 判斷是否為存託憑證資料，如果是，則跳過此次迴圈
            if "存託憑證" in cols_data[3]:  # 產業類別是資料中的第四列
                continue
            
            # 將提取的資料添加到表格資料列表中
            table_data.append(cols_data)

    # 設定 CSV 檔案路徑
    csv_file_path = "./stock_info/sii_stock_info.csv"

    # 將表格資料寫入 CSV 檔案
    with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        # 使用 csv 模組寫入 CSV 檔案
        writer = csv.writer(csvfile)
        
        # 先寫入標題行
        writer.writerow(column_names)
        
        # 寫入表格內容
        writer.writerows(table_data)

    print(f'{market_type}資料已成功儲存到', csv_file_path)

    # 讀取剛剛存入的 CSV 檔案
    df = pd.read_csv(csv_file_path)
    
    # 替換 '-' 為 '無'
    df.replace('-', '無', inplace=True)
    
    # 替換 NaN (空值) 為 '無'
    df.fillna('無', inplace=True)

    # 儲存替換後的資料回到原CSV檔案
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

    # 讀取剛剛存入的 CSV 檔案
    sii_column_names = ["股票代碼", "公司名稱", "公司簡稱", "產業類別", "住址",  "董事長", "成立日期", "上市日期", "普通股每股面額", "實收資本額(元)", 
                        "已發行普通股數或TDR原發行股數", "編製財務報告類型", "普通股盈餘分派或虧損撥補頻率", 
                        "普通股年度(含第4季或後半年度)現金股息及紅利決議層級", "股票過戶機構", "簽證會計師事務所", "英文簡稱", "電子郵件信箱", "公司網址"]
    
    # 選擇指定的欄位
    selected_columns = df[sii_column_names]

    # 將選擇的資料存入原 CSV 檔案
    selected_columns.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

    print(f'選擇的{market_type}資料已成功更新回', csv_file_path)

finally:
    # 關閉瀏覽器
    driver.quit()

# 設定指定股票代碼檔案的路徑
stock_codes_path = r'C:\Users\yingh\Desktop\python爬蟲\50股.xlsx'

# 讀取指定股票代碼
stock_codes_df = pd.read_excel(stock_codes_path)
stock_codes = stock_codes_df['股票代碼'].tolist()  # 假設股票代碼欄位名稱為 "股票代碼"

# 從已存的 CSV 中讀取資料
filtered_df = pd.read_csv(csv_file_path)

# 篩選出符合指定股票代碼的資料
filtered_df = filtered_df[filtered_df['股票代碼'].isin(stock_codes)]

# 設定篩選後的 CSV 檔案路徑
filtered_csv_path = './stock_info/sii_stock_info_filtered.csv'

# 將篩選後的資料寫入新的 CSV 檔案
filtered_df.to_csv(filtered_csv_path, index=False, encoding='utf-8-sig')

print(f'篩選後的資料已成功儲存到 {filtered_csv_path}')