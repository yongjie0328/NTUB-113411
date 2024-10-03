import pandas as pd
import jieba

def load_sentiment_dict_from_file(positive_filepath, negative_filepath):
    sentiment_dict = {}

    # 正面情感詞
    with open(positive_filepath, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            if word:
                sentiment_dict[word] = 1  # 正面詞得分為 1

    # 負面情感詞
    with open(negative_filepath, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            if word:
                sentiment_dict[word] = -1  # 負面詞得分為 -1
    
    return sentiment_dict

# 確保檔案路徑正確
sentiment_dict = load_sentiment_dict_from_file('C:/Users/yingh/Desktop/python爬蟲/stock_news/ntusd-positive.txt', 'C:/Users/yingh/Desktop/python爬蟲/stock_news/ntusd-negative.txt')

def analyze_sentiment_jieba(text, sentiment_dict):
    # 使用jieba進行分詞
    words = jieba.lcut(text)
    
    # 計算情感得分
    score = sum(sentiment_dict.get(word, 0) for word in words)
    
    # 簡單分類
    if score > 0:
        sentiment = '正面'
    elif score < 0:
        sentiment = '負面'
    else:
        sentiment = '中性'
    
    return sentiment, score

# 讀取新聞數據
df = pd.read_csv('./stock_news/tw_stock_news.csv')

# 定義一個函數來處理每一行
def analyze_row(row):
    sentiment, score = analyze_sentiment_jieba(row['內容'], sentiment_dict)
    return pd.Series([sentiment, score], index=['情感分類', '情感得分'])

# 應用到數據框
df[['情感分類', '情感得分']] = df.apply(analyze_row, axis=1)

# 儲存结果
df.to_csv('./stock_news/tw_stock_news_jieba.csv', index=False, encoding='utf-8-sig')
print("情感分析结果已儲存。")