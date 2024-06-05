from datetime import datetime, timedelta
import pandas as pd
import requests
import time
import html
import re

def clean_html_tags(text):
    """ 去除HTML标签 """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def save_to_csv(newslist_info, filename='./stock_news/tw_stock_news.csv'):
    data = []
    for page in newslist_info:
        for news in page["data"]:
            content = html.unescape(news['content'])  # 将 HTML 实体转换为普通文本
            content = clean_html_tags(content)  # 去除 HTML 标签
            data.append({
                '新聞編號': news['newsId'],
                '網址': f'https://news.cnyes.com/news/id/{news["newsId"]}',
                '標題': news['title'],
                '摘要': news['summary'],
                '關鍵字': news['keyword'],
                '內容': content,
                '發布時間': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(news["publishAt"])),
                '類別': news['categoryName'],
                '類別號碼': news['categoryId']
            })

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')

class TaiwanStockNewsSpider:
    def get_newslist_info(self, start_time=None, end_time=None, limit=30):
        headers = {
            'Origin': 'https://news.cnyes.com/news/cat/tw_stock',
            'Referer': 'https://news.cnyes.com/news/cat/tw_stock',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        
        all_newslist_info = []
        params = {
            'page': 1,
            'limit': limit,
            'startAt': start_time,
            'endAt': end_time
        }
        
        r = requests.get(f"https://api.cnyes.com/media/api/v1/newslist/category/tw_stock", headers=headers, params=params)
        newslist_info = r.json().get('items')
        limit_page = newslist_info["last_page"]

        for page in range(1, limit_page + 1):
            params['page'] = page
            r = requests.get(f"https://api.cnyes.com/media/api/v1/newslist/category/tw_stock", headers=headers, params=params)
            newslist_info = r.json().get('items')
            filtered_news = [news for news in newslist_info["data"] if news["categoryName"] not in ["ETF", "台灣政經"]]
            all_newslist_info.append({"data": filtered_news, "page": page})

        return all_newslist_info

if __name__ == "__main__":
    taiwan_stock_news_spider = TaiwanStockNewsSpider()

    now = datetime.now()
    start_time = now - timedelta(days=7)
    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(now.timestamp())

    newslist_info_all = taiwan_stock_news_spider.get_newslist_info(start_timestamp, end_timestamp)
    
    for newslist_info in newslist_info_all:
        if newslist_info is not None:
            print(f'搜尋結果 > 當前頁數：{newslist_info["page"]}')
            for news in newslist_info["data"]:
                content = html.unescape(news["content"])  # 将 HTML 实体转换为普通文本
                content = clean_html_tags(content)  # 去除 HTML 标签
                print(f'    ------------ {news["newsId"]} ------------')
                print(f'    新聞 > 網址：https://news.cnyes.com/news/id/{news["newsId"]}')
                print(f'    新聞 > 標題：{news["title"]}')
                print(f'    新聞 > 摘要：{news["summary"]}')
                print(f'    新聞 > 內容：{content}')
                print(f'    新聞 > 關鍵字：{news["keyword"]}')
                print(f'    新聞 > 發布時間：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(news["publishAt"]))}')
                print(f'    新聞 > 類別：{news["categoryName"]} (id:{news["categoryId"]})')

    if newslist_info_all is not None:
        save_to_csv(newslist_info_all)
        print("國內新聞的資料已成功存入 './stock_news/tw_stock_news.csv' 檔案。")

    df = pd.read_csv('./stock_news/tw_stock_news.csv')

    # 將所有NaN值替換為"無"
    df.fillna('無', inplace=True)

    df.to_csv('./stock_news/tw_stock_news.csv', index=False, encoding='utf-8-sig')
    print("修改後的資料已成功存回 './stock_news/tw_stock_news.csv' 檔案中。")

