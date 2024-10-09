from googletrans import Translator
import pandas as pd
import time
import re

# 讀取 CSV 文件
file_path = r'C:\Users\yingh\Desktop\python爬蟲\stock_news\int_stock_news.csv'  # 請替換為你的文件路徑
df = pd.read_csv(file_path)

# 創建翻譯器
translator = Translator()

# 定義翻譯函數
def translate_text(text):
    if pd.isna(text):  # 處理缺失值
        return text
    if isinstance(text, str) and len(text.strip()) > 0:  # 確保是有效的字串
        if re.match(r'^https?://', text):  # 檢查是否是 URL
            print(f"跳過 URL: {text}")
            return text  # 跳過 URL，不進行翻譯
        try:
            translated = translator.translate(text, src='en', dest='zh-tw')  # 從英文翻譯到繁體中文
            time.sleep(1)  # 每次請求後暫停 1 秒，以防速率限制
            return translated.text
        except Exception as e:  # 捕獲所有異常
            print(f"翻譯失敗: {text}, 錯誤信息: {e}")
            return text  # 返回原文本以便後續處理
    else:
        print(f"跳過無效內容: {text}")
        return text  # 返回原文本以便後續處理

# 遍歷 DataFrame 的每一列，並對每個單元格進行翻譯
for column in df.columns:
    df[column] = df[column].apply(translate_text)

# 保存到新的 CSV 文件
output_file_path = r'C:\Users\yingh\Desktop\python爬蟲\stock_news\int_stock_news_translated.csv'  # 輸出文件路徑
df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print("翻譯完成並已保存到新的 CSV 文件！")