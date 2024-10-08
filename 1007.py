from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import yfinance as yf  # 引入 yfinance 库

app = Flask(__name__)
CORS(app)

# 設定 OpenAI API 金鑰
openai.api_key = ''

# 新手小學堂知識庫
knowledge_base = {
     "什麼是股票": "股票是公司發行的股份，代表持有人擁有公司的一部分權益。當你購買公司的股票時，你實際上成為了該公司的部分所有者。",
    "股票代碼": "股票代碼（Stock Symbol），又稱股票代號，是用來標識特定公司的簡短字母或數字組合。每家上市公司的股票都有一個唯一的股票代碼，用於在證券交易所進行交易。",
    "股票價格": "看盤時我們所看到的是股票單價，也就是每一股的價格。而股票的成交價通常是由市場的買方、賣方共同決定，但不像房屋交易那樣會有房屋仲介媒合，股票通常是由證券交易所的電腦系統進行撮合。",
    "股票交易時間": "股票市場並非24小時都開放，通常會有指定開放交易的時間。以台灣為例，股票市場的交易時間為每週一至週五的9:00～13:30，盤後定價交易時間為14:00～14:30，而零股盤後交易時間為13:40～14:30。",
    "股票買賣單位": "在台灣股票市場中，股票的基本買賣單位是一張，每張股票代表1000股。如果投資者希望買賣少於一張（即1000股）的股票，可以通過零股交易進行，選擇購買1～999股。",
    "上市、上櫃、興櫃": "世界各國的股票市場大致分為上市、上櫃、興櫃三種，台灣股市也不例外。最簡單區分上市、上櫃、興櫃的方法是觀察「最低實收資本額」，興櫃公司若高於門檻就能往上櫃前進，以此類推。",
    "三大法人": "在台灣股票市場，三大法人指的是市場上主要的機構投資者，分別是外資、投信和自營商，這些法人對股市的影響力非常大。",
    "股票獲利方式": "投資股票獲利最主要為兩種：1. 股票賺價差：股價上漲並賺取股票價差；2. 股息：公司賺錢時，把獲利的一部分分給股東。",
    "股票交易成本": "股票交易成本主要有三種：1. 手續費：購買金額的0.1425%，未滿20元按20元計收；2. 交易稅：賣出台股時需付0.30%的交易稅；3. 股利所得稅：參與除權息並收到現金股利時需課稅。",
    "股票類型": "股票類型可分為市值、產業類別和特性等。市值可分為大盤股和中小盤股；產業類別可參考產業價值鏈資訊平台；股票特性有藍籌股、成長股、價值股、週期股等。",
    "系統功能": "教學小學堂、AI預測股價、國內外新聞、投資組合計算器、股票價格追蹤功能",
    "系統股票總類" : "金融保險類、半導體業、航運類、電腦及週邊設備業、光電業",
    "系統金融保險業":"2888新光金、2891中信金、2883開發金、2882國泰金控、2867三商壽、2884玉山金控、2880華南金控、2890永豐金控、2834臺灣企銀、2885元大金",
    "系統半導體業":"2303聯電、2363矽統、2330台積電、6770力積電、2344華邦電、2449京元電子、4967十詮、2408南亞科、3450聯均、3711日月光投控",
    "系統航運業":"2618長榮航、2609陽明、2610華航、2603長榮、2615萬海、2605新興、2634漢翔、2606裕民、5608四維航、2637慧洋-KY",
    "系統電腦及週邊設備業":"3231緯創、2353宏碁、2382廣達、2356英業達、3013晟銘電、2324仁寶、2301中鋼、2365昆盈、3017奇鋐、3706神達",
    "系統光電業":"2323中環、2349錸德、2374佳能、2393億光、2406國碩、2409友達、2426鼎元、2429銘旺科、2438翔耀、2466冠西電",

}

# 查詢知識庫
def query_knowledge_base(question):
    for key in knowledge_base:
        if key in question:
            return knowledge_base[key]
    return None

# 使用 Yahoo Finance 查詢股票價格
def get_stock_price(symbol):
    try:
        # 如果符號是純數字，假設為台股，添加 .TW 後綴
        if symbol.isdigit():
            symbol += '.TW'

        print(f"Fetching stock data for: {symbol}")  # 调试信息
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period='1d')
        print(f"Stock info: {stock_info}")  # 调试信息

        if not stock_info.empty:
            latest_price = stock_info['Close'].iloc[-1]
            return f"{symbol} 今天的最新股價是 {latest_price:.2f} 元。"
        else:
            return f"無法獲取 {symbol} 的股價，可能是因為該股票代碼不正確或無法訪問即時數據。"
    except Exception as e:
        print(f"發生錯誤：{str(e)}")
        return "無法取得股票價格，請確認網路連線是否正常，或者嘗試使用其他股票代碼。"

# 使用 OpenAI API 生成回答
def get_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個會說繁體中文的有幫助的助手。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"發生錯誤：{str(e)}")
        return f"發生錯誤，請稍後再試：{str(e)}"

# 定義 Flask 路由來處理前端的問答請求
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    user_question = data.get('question', '')

    if not user_question:
        return jsonify({'answer': '請輸入問題。'}), 400

    # 優先查詢知識庫
    knowledge_base_answer = query_knowledge_base(user_question)
    if knowledge_base_answer:
        return jsonify({'answer': knowledge_base_answer})

    # 查詢股票價格
    if "股價" in user_question:
        # 查找问题中的股票代码
        symbol = ''.join(filter(str.isdigit, user_question))
        if symbol:
            stock_price_answer = get_stock_price(symbol)
            return jsonify({'answer': stock_price_answer})

    # 調用 OpenAI 生成回答
    response = get_response(user_question)
    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True)
