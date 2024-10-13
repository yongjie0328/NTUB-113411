from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import jieba
import os

# 讀取 CSV 文件
file_path = 'C:/Users/yingh/Desktop/python爬蟲/stock_news/tw_stock_news_jieba.csv'
df = pd.read_csv(file_path)

# 獲取文本數據
text_data = df['內容'].dropna().tolist()
text = ' '.join(text_data)

# 分詞
wordlist = jieba.cut(text, cut_all=False)
word_space_split = " ".join(wordlist)

# 停用詞列表，包含"的"等不需要出現在文字雲中的詞
stopwords = set(['的', '是', '在', '和', '也', '為', '有', '於', '與', '及', '而', '或', '以', '都', '等', '了'])

# 移除停用詞
filtered_words = [word for word in word_space_split.split() if word not in stopwords]
filtered_text = " ".join(filtered_words)

# 設定字體路徑
font_path = "SimHei.ttf"
if not os.path.exists(font_path):
    font_path = "C:\\Users\\yingh\\Downloads\\simhei\\SimHei.ttf"

# 生成文字雲
wordcloud = WordCloud(font_path=font_path, width=800, height=400).generate(filtered_text)

# 顯示文字雲
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")

# 保存圖片到指定資料夾
output_path = 'C:/Users/yingh/Desktop/python爬蟲/stock_news/tw_stock_wordcloud.png'
plt.savefig(output_path)

# 顯示圖片並打印確認訊息
plt.show()
print(f"文字雲圖片已儲存到: {output_path}")