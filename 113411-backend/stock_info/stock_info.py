import csv
import time 
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 設定瀏覽器驅動程式路徑
driver_path = r'C:\Users\yingh\Desktop\python爬蟲\chromedriver.exe'

# 初始化 Chrome 瀏覽器
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# 設定等待時間
wait = WebDriverWait(driver, 10)

# 前往網頁
driver.get("https://mops.twse.com.tw/mops/web/t51sb01")

# 市場類型列表
market_types = ['上市', '上櫃']

try:
    for market_type in market_types:
        # 找到市場類型下拉選單
        market_select = Select(driver.find_element(By.XPATH, "//select[@name='TYPEK']"))

        # 選擇市場類型
        market_select.select_by_visible_text(market_type)

        # 顯示資料載入中，請稍後..
        wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='code']//option")))

        # 找到產業類型下拉選單
        industry_select = Select(driver.find_element(By.XPATH, "//select[@name='code']"))

        # 選擇產業類型選項
        industry_select.select_by_index(0) # 選擇第一個選項，空值為查詢全部產業類型

        # 點擊查詢按鈕
        search_button = driver.find_element(By.XPATH, "//input[@value=' 查詢 ']")
        search_button.click()

        # 等待查詢結果加載完成
        time.sleep(10)  # 這裡等待10秒，可以根據頁面加載速度進行調整

        # 獲取網頁的原始碼
        html_content = driver.page_source

        # 使用BeautifulSoup模組解析網頁
        soup = BeautifulSoup(html_content, 'html.parser')

        if market_type == '上市':
            # 將表頭欄位名稱指定給 column_names 變數
            column_names = ["公司代號", "公司名稱", "公司簡稱", "產業類別", "外國企業註冊地國", "住址", "營利事業統一編號", "董事長", "總經理",
                            "發言人", "發言人職稱", "代理發言人", "總機電話", "成立日期", "上市日期", "普通股每股面額", "實收資本額(元)",
                            "已發行普通股數或TDR原發行股數", "私募普通股(股)", "特別股(股)", "編製財務報告類型", "普通股盈餘分派或虧損撥補頻率",
                            "普通股年度(含第4季或後半年度)現金股息及紅利決議層級", "股票過戶機構", "過戶電話", "過戶地址", "簽證會計師事務所",
                            "簽證會計師1", "簽證會計師2", "英文簡稱", "英文通訊地址", "傳真機號碼", "電子郵件信箱", "公司網址", "投資人關係聯絡人",
                            "投資人關係聯絡人職稱", "投資人關係聯絡電話", "投資人關係聯絡電子郵件", "公司網站內利害關係人專區網址"]
        else:
            # 將表頭欄位名稱指定給 column_names 變數
            column_names = ["公司代號", "公司名稱", "公司簡稱", "產業類別", "外國企業註冊地國", "住址", "營利事業統一編號", "董事長", "總經理",
                            "發言人", "發言人職稱", "代理發言人", "總機電話", "成立日期", "上櫃日期", "普通股每股面額", "實收資本額(元)",
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
            if len(cols1,) == len(column_names):
                # 提取每一列的資料，並去除空白字符
                cols_data = [col.text.strip() for col in cols1]
                # 將提取的資料添加到表格資料列表中
                table_data.append(cols_data)

        # 設定 CSV 檔案路徑
        if market_type == '上市':
            csv_file_path = "sii_stock_info.csv"
        else:
            csv_file_path = "otc_stock_info.csv"

        # 將表格資料寫入 CSV 檔案
        with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # 使用 csv 模組寫入 CSV 檔案
            writer = csv.writer(csvfile)
            
            # 先寫入標題行
            writer.writerow(column_names)
            
            # 寫入表格內容
            writer.writerows(table_data)  # 將 DataFrame 轉換為列表後寫入

        print("表格資料已成功儲存到:", csv_file_path)

        # 檔案路徑
        if market_type == '上市':        
            # 讀取剛剛存入的 CSV 檔案
            df = pd.read_csv(csv_file_path)

            column_names2= ["公司代號", "公司名稱", "公司簡稱", "產業類別", "住址",  "董事長", "成立日期", "上市日期", "普通股每股面額", "實收資本額(元)", 
                            "已發行普通股數或TDR原發行股數", "編製財務報告類型", "普通股盈餘分派或虧損撥補頻率", 
                            "普通股年度(含第4季或後半年度)現金股息及紅利決議層級", "股票過戶機構", "簽證會計師事務所", "英文簡稱", "電子郵件信箱", "公司網址"]
            # 選擇指定的欄位
            selected_columns = df[column_names2]

            # 新的 CSV 檔案路徑
            sii_stock_info_file_path = "sii_stock_info_select.csv"

            # 將選擇的資料存入新的 CSV 檔案
            selected_columns.to_csv(sii_stock_info_file_path, index=False, encoding='utf-8-sig')

            print("選擇的資料已成功儲存到:", sii_stock_info_file_path)
        else:
            df = pd.read_csv(csv_file_path)
            column_names2= ["公司代號", "公司名稱", "公司簡稱", "產業類別", "住址", "董事長", "成立日期", "上櫃日期", "普通股每股面額", "實收資本額(元)", 
                            "已發行普通股數或TDR原發行股數", "編製財務報告類型", "普通股盈餘分派或虧損撥補頻率", 
                            "普通股年度(含第4季或後半年度)現金股息及紅利決議層級", "股票過戶機構", "簽證會計師事務所", "英文簡稱", "電子郵件信箱", "公司網址"]
            # 選擇指定的欄位
            selected_columns = df[column_names2]

            # 新的 CSV 檔案路徑
            otc_stock_info_file_path = "otc_stock_info_select.csv"

            # 將選擇的資料存入新的 CSV 檔案
            selected_columns.to_csv(otc_stock_info_file_path, index=False, encoding='utf-8-sig')

            print("選擇的資料已成功儲存到:", otc_stock_info_file_path)

finally:
    # 關閉瀏覽器
    driver.quit()