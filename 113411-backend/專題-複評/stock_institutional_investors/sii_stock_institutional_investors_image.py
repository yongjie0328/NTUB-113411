import matplotlib.pyplot as plt
import pandas as pd
import os

# 設置字體，解決負號顯示問題
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

# 讀取 CSV 檔案
file_path = r'C:\Users\yingh\Desktop\python爬蟲\stock_institutional_investors\sii_stock_institutional_investors_filtered.csv'
df = pd.read_csv(file_path)

# 獲取所有股票代碼
stock_codes = df['股票代碼'].unique()

# 轉換民國年到西元年
def convert_date(date_int):
    # 將整數轉換為字串
    date_str = str(date_int)
    # 將字串格式轉換為“YYYY/MM/DD”
    formatted_date = f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:]}"
    return formatted_date

df['日期'] = df['日期'].apply(convert_date)
df['日期'] = pd.to_datetime(df['日期'], format='%Y/%m/%d')

# 數據清理並轉換為數值型
df['外陸資買賣超股數(不含外資自營商)'] = pd.to_numeric(df['外陸資買賣超股數(不含外資自營商)'].str.replace(',', ''), errors='coerce')
df['投信買賣超股數'] = pd.to_numeric(df['投信買賣超股數'].str.replace(',', ''), errors='coerce')
df['自營商買賣超股數'] = pd.to_numeric(df['自營商買賣超股數'].str.replace(',', ''), errors='coerce')

# 定義繪圖函數
def plot_institutional_data(data, institution_name, column_name,column_name_2, ax):
    if column_name_2==0:
        ax.bar(data['日期'], data[column_name], color=['red' if x >= 0 else 'green' for x in data[column_name]], width=1.0)
        ax.axhline(0, color='gray', linewidth=0.8)
        ax.set_ylabel('買賣超股數')
        ax.set_title(f'{institution_name} 買賣超股數走勢圖')
    else:
        ax.bar(data['日期'], data[column_name]+data[column_name_2], color=['red' if x >= 0 else 'green' for x in data[column_name]+data[column_name_2]], width=1.0)
        ax.axhline(0, color='gray', linewidth=0.8)
        ax.set_ylabel('買賣超股數')
        ax.set_title(f'{institution_name} 買賣超股數走勢圖')

# 為每個股票代碼生成圖表
output_dir = r'C:\Users\yingh\Desktop\python爬蟲\stock_institutional_investors\sii_stock_institutional_investors_image'  # 將此路徑替換為你已有的文件夾路徑

for code in stock_codes:
    filtered_df = df[df['股票代碼'] == code].copy()
    
    # 取得股票名稱 (假設 df 中有 '證券名稱' 欄位)
    stock_name = filtered_df['證券名稱'].iloc[0]  

    # 選擇所需的列
    selected_columns = ['日期', '股票代碼', '外陸資買賣超股數(不含外資自營商)', '外資自營商買賣超股數', '投信買賣超股數', '自營商買賣超股數']
    result_df = filtered_df[selected_columns]

    # 繪製圖表
    fig, axes = plt.subplots(3, 1, figsize=(14, 8), sharex=True)

    plot_institutional_data(result_df, '外資及陸資', '外陸資買賣超股數(不含外資自營商)','外資自營商買賣超股數', axes[0])
    plot_institutional_data(result_df, '投信', '投信買賣超股數',0 , axes[1])
    plot_institutional_data(result_df, '自營商', '自營商買賣超股數',0,  axes[2])

    plt.xticks(rotation=45)
    plt.xlabel('日期')

    # 添加圖表標題，包括股票代碼和名稱
    fig.suptitle(f'{str(code).strip()}{stock_name.strip()}的三大法人買賣超股數走勢圖', fontsize=16)

    plt.tight_layout(rect=[0, 0, 1, 0.96])  

    # 保存圖表為文件
    file_name = os.path.join(output_dir, f'{code}_chart.png')
    plt.savefig(file_name)
    plt.close(fig)

    print(f'圖片已儲存到: {file_name}')