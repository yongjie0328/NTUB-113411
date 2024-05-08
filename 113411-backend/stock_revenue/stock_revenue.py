import pandas as pd
import requests

# 定義日期的年度與月份
date = '113_4'

def crawl_stock_data(url):
    res = requests.get(url)
    res.encoding = 'big5'
    html_df = pd.read_html(res.text)           

    # 去除行數錯誤的表格，並合併表格
    df = pd.concat([df for df in html_df if df.shape[1] == 11]) 

    # 設置表頭
    df.columns = df.columns.get_level_values(1)

    # 去除多餘列, 重新排序索引
    df = df[df['公司名稱'] != '合計']
    df = df.reset_index(drop=True) 

    return df

def save_stock_data(df, filename):
    # 將浮點數格式化為含千分位逗號的字串
    df_formatted = df.applymap(lambda x: '{:,.0f}'.format(x) if isinstance(x, (int, float)) else x)

    # 將 DataFrame 儲存為 CSV 檔案，並指定浮點數輸出格式
    df_formatted.to_csv(filename, index=False, encoding='utf-8-sig', float_format='%.0f')
    print(f"資料已成功儲存到 '{filename}' 檔案中。")

# 爬取股票資料並儲存到對應的檔案中
stock_urls = {
    'tw_sii': f'https://mops.twse.com.tw/nas/t21/sii/t21sc03_{date}_0.html', #國內上市股票
    'int_sii': f'https://mops.twse.com.tw/nas/t21/sii/t21sc03_{date}_1.html', #國外上市股票
    'tw_otc': f'https://mops.twse.com.tw/nas/t21/otc/t21sc03_{date}_0.html', #國內上櫃股票
    'int_otc': f'https://mops.twse.com.tw/nas/t21/otc/t21sc03_{date}_1.html' #國外上櫃股票
}

for category, url in stock_urls.items():
    df = crawl_stock_data(url)
    filename = f"{category}_stock_revenue.csv"
    save_stock_data(df, filename)