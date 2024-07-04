from datetime import datetime, timedelta
import pandas as pd
import requests

#上市股票除權息歷史資料
def get_twse_dividend_history(start_date: str, end_date: str):
    url = f"https://www.twse.com.tw/exchangeReport/TWT49U?response=html&strDate={start_date}&endDate={end_date}"
    dividend_history = pd.read_html(url)
    return dividend_history[0]

#上櫃股票除權息歷史資料
def get_tpex_dividend_history(start_date: str, end_date: str):
    # 將日期格式從 YYYYMMDD 轉換為 YYY/MM/DD
    start_date = f"{int(start_date[:4])-1911}/{start_date[4:6]}/{start_date[6:]}"
    end_date = f"{int(end_date[:4])-1911}/{end_date[4:6]}/{end_date[6:]}"
    url = f"https://www.tpex.org.tw/web/stock/exright/dailyquo/exDailyQ_result.php?l=zh-tw&d={start_date}&ed={end_date}"

    dividend_history_columns = [
        "除權息日期", "代號", "名稱", "除權息前收盤價", "除權息參考價", "權值", "息值", "權值+息值",
        "權/息", "漲停價", "跌停價", "開始交易基準價", "減除股利參考價", "現金股利",
        "每仟股無償配股", "現金增資股數", "現金增資認購價", "公開承銷股數", "員工認購股數",
        "原股東認購股數", "按持股比例仟股認購",
    ]
    res = requests.get(url)
    dividend_history = pd.DataFrame(res.json()["aaData"], columns=dividend_history_columns)
    return dividend_history

# 定義日期範圍（過去30天）
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
end_date_str = end_date.strftime("%Y%m%d")
start_date_str = start_date.strftime("%Y%m%d")

# 儲存上市股票除權息歷史資料
twse_dividend_history = get_twse_dividend_history(start_date_str, end_date_str)
twse_dividend_history.to_csv("./stock_dividend/sii_stock_dividend.csv", index=False, encoding='utf-8-sig')
print("上市股票除權息歷史資料已儲存到 './stock_dividend/sii_stock_dividend.csv' 檔案。")

# 儲存上櫃股票除權息歷史資料
two_dividend_history = get_tpex_dividend_history(start_date_str, end_date_str)
two_dividend_history.to_csv("./stock_dividend/otc_stock_dividend.csv", index=False, encoding='utf-8-sig')
print("上櫃股票除權息歷史資料已儲存到 './stock_dividend/otc_stock_dividend.csv' 檔案。")