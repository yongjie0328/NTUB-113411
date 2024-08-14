import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from nltk.corpus import stopwords
import nltk
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 下載 NLTK 資源
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# 1. 爬取主頁上的所有新闻網址
def fetch_news_links(url, limit=20):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查請求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')

        # 尋找所有 <a> 標籤並過濾掉非新闻網址
        links = soup.find_all('a')
        news_links = []
        for link in links:
            href = link.get('href')
            if href and 'https://finance.yahoo.com/news/' in href:
                news_links.append(href)
            if len(news_links) >= limit:  # 限制爬取的數量
                break

        # 去重
        news_links = list(set(news_links))
        
        print(f"Found news links: {news_links}")  
        return news_links
    except Exception as e:
        print(f"An error occurred while fetching the news links: {e}")
        return []

# 2. 爬取單個新聞内容
def fetch_news(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查請求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')

        # 根據特定的 class 名稱提取標題
        title_tag = soup.find(class_='caas-title-wrapper')
        title = title_tag.get_text() if title_tag else 'No title found'
        
        # 提取内容
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])

        # 生成摘要（取前几句）
        summary = ' '.join(content.split()[:50])

        return title, content, summary
    except Exception as e:
        print(f"An error occurred while fetching the news: {e}")
        return None, None, None

# 3. 關键字提取
def extract_keywords(text):
    blob = TextBlob(text)
    words = blob.words
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word.lower() not in stop_words and word.isalpha()]
    return keywords

# 4. 情绪分析
def sentiment_analysis(text):
    try:
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        
        # Define thresholds for positive and negative sentiment
        if sentiment > 0.1:
            sentiment_label = "positive"
        elif sentiment < -0.1:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        
        return sentiment_label
    except Exception as e:
        print(f"An error occurred while performing sentiment analysis: {e}")
        return "unknown"

# 5. 生成文字雲
def generate_wordcloud(text, filename='wordcloud.png'):
    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(filename)
    print(f"Wordcloud saved as {filename}")
    plt.show()

# 6. 保存數據到 Excel
def save_to_excel(data, filename):
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving data to Excel: {e}")

# 主流程
def main():
    homepage_url = 'https://finance.yahoo.com/topic/stock-market-news/'  # Yahoo Finance 主頁的 URL
    news_links = fetch_news_links(homepage_url)

    all_news_data = []
    all_keywords = []  # 用於存儲所有關鍵字
    for url in news_links:
        print(f"正在處理新聞: {url}\n")
        title, content, summary = fetch_news(url)
        
        if title and content:
            print(f"標題: {title}\n")
            print(f"摘要: {summary}\n")

            keywords = extract_keywords(content)
            print(f"關键字: {', '.join(keywords[:10])}\n")  # 顯示前10個關鍵字

            all_keywords.extend(keywords)  # 保存所有關鍵字

            sentiment_label = sentiment_analysis(content)
            print(f"情绪分析 - 分類: {sentiment_label}\n")

            # 收集所有新聞的數據
            all_news_data.append({
                'URL': url,
                'Title': title,
                'Summary': summary,
                'Keywords': ', '.join(keywords[:10]),
                'Sentiment': sentiment_label
            })
        else:
            print("無法提取新聞内容。\n")

    # 生成並保存文字雲
    generate_wordcloud(' '.join(all_keywords))

    # 保存所有新聞數據到 Excel 文件
    save_to_excel(all_news_data, 'news_data.xlsx')

if __name__ == "__main__":
    main()
