<template>
  <div class="news-and-cloud">

    <div class="news-section">
      <h1>新聞區</h1>
      <!-- 添加兩個按鈕 -->
      <div class="news-buttons">
        <button :class="{ 'active': selectedNews === 'domestic' }" @click="showNews('domestic')">國內新聞</button>
        <button :class="{ 'active': selectedNews === 'international' }" @click="showNews('international')">國外新聞</button>
      </div>
      <!-- 根據 selectedNews 顯示新聞 -->
      <div v-if="selectedNews === 'domestic'">
        <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5585734" target="_blank" rel="noopener noreferrer"
              class="newstit">《價值型投資 最新產業研究報告》COMPUTEX 2024正式起跑 輝達執行長黃仁勳先行點名圓剛</a></h3>
          <p>摘要:無</p>
          <P>發布時間:2024-06-04 14:02:26</P>
          <span class="positive">關鍵字: ['蔡慶龍', '價值型投資', '圓剛', '主流績優股', '趨勢分析', '摩爾投顧']</span>
        </div>
        <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5585713" target="_blank" rel="noopener noreferrer"
              class="newstit">〈台股盤後〉輝達夥伴、權值股漲累了  回檔修正跌180點收21356點</a></h3>
          <p>摘要:台股昨 (3) 日大漲超過 300 點，今 (4) 日開高走低回檔修正，跌逾 200 點，權值股以及輝達 (NVDA-US) 供應鏈夥伴普遍走弱，終場跌 180.14 點或 0.84%，以 21356.62 點作收，成交量 4419.57 億元。</p>
          <P>發布時間:2024-06-04 14:03:20</P>
          <span class="positive">關鍵字:['台股盤後', '台積電', '輝達', 'AI']</span>
        </div>
        <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5585672" target="_blank" rel="noopener noreferrer"
              class="newstit">〈COMPUTEX〉廣運在智慧倉儲系統接單強勁 估將超越逾50%營收比重</a></h3>
          <p>摘要:除新一代水冷散熱系統及半導體自動化設備之外，廣運 (6125-TW) 今 (4) 日出席台北 COMPUTEX 展，總經理柯智鈞也對包含客製化工廠自動化生產線、自動倉儲系統、電商物流發貨中心等的大量接單表示樂觀。</p>
          <P>發布時間:2024-06-04 13:12:25</P>
          <span class="positive">關鍵字:['廣運', '鴻海', '巨大', 'COMPUTEX']</span>
        </div>
        <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5585671" target="_blank" rel="noopener noreferrer"
              class="newstit">〈COMPUTEX〉黃仁勳參訪鴻佰攤位 稱鴻海是輝達GB200最重要合作夥伴</a></h3>
          <p>摘要:黃仁勳參訪鴻佰攤位 稱鴻海是輝達 GB200 最重要的合作夥伴</p>
          <P>發布時間:2024-06-04 13:48:44</P>
          <span class="positive">關鍵字:['輝達', '黃仁勳', '鴻海', '鴻佰', 'GB200']</span>
        </div>
         <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5585651" target="_blank" rel="noopener noreferrer"
              class="newstit">〈COMPUTEX〉長榮航攜手貿協參展 擴大爭取企業戶</a></h3>
          <p>摘要:長榮航與外貿協會攜手參加電腦展 擴大爭取企業戶</p>
          <P>發布時間:2024-06-04 12:58:21</P>
          <span class="positive">關鍵字:['長榮航', '外貿協會', 'computex', '電腦展']</span>
        </div>
        <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5585620" target="_blank" rel="noopener noreferrer"
              class="newstit">鉅亨速報 - Factset 最新調查：和碩(4938-TW)目標價調升至93.5元，幅度約3.21%</a></h3>
          <p>摘要:FactSet 最新調查：和碩(4938-TW)目標價調升，最高估值、最低估值、中位數、綜合評級、近5日股價、大盤表現、即時新聞資訊。</p>
          <P>發布時間:2024-06-04 13:00:45</P>
          <span class="positive">關鍵字:['AI', '求職', '1111']</span>
        </div>
        <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5585573" target="_blank" rel="noopener noreferrer"
              class="newstit">〈COMPUTEX〉輝達未來5年在台設立研發中心 黃仁勳：這三地是選項</a></h3>
          <p>摘要:輝達 (NVDA-US) 執行長黃仁勳今 (4) 日到 COMPUTEX 與供應鏈夥伴們會面，黃仁勳接受媒體訪問談到未來 5 年將在台灣設立、投資研發中心，黃仁勳強調，台灣已經輝達很大的基地，同時也透露台北、台南以及高雄都會是選項。</p>
          <P>發布時間:2024-06-04 12:16:07</P>
          <span class="positive">關鍵字:['黃仁勳', 'AI', '伺服器', 'COMPUTEX']</span>
        </div>
        <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5585542" target="_blank" rel="noopener noreferrer"
              class="newstit">廣運籌資擬發行 6 億元無擔保CB明起競拍 6/21掛牌</a></h3>
          <p>摘要:廣運業績可望升同時，廣運向金管會送件辦理發行 1 萬張的現增股，同時，擬發行 6 億元的無擔保可轉換公司債 (CB) 已經申報生效，其中，擬發行 CB 籌資案完成訂價，轉換價訂為 114 元。</p>
          <P>發布時間:2024-06-04 11:48:37</P>
          <span class="positive">關鍵字:['廣運', '辛耘', 'CB', '籌資']</span>
        </div>
        <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5585540" target="_blank" rel="noopener noreferrer"
              class="newstit">Gogoro獲潤泰注資5000萬美元 推展全球業務</a></h3>
          <p>摘要:Gogoro 獲潤泰注資 5000 萬美元 推展全球業務</p>
          <P>發布時間:2024-06-04 11:40:03</P>
          <span class="positive">關鍵字:['gogoro', '潤泰', '電動車', '充電', '機車']</span>
        </div>
      
      </div>


      <div v-if="selectedNews === 'international'">
        <div class="news-card">
          <h3><a href="https://finance.yahoo.com/news/mccormick-stock-gains-q3-earnings-122822550.html" target="_blank" rel="noopener noreferrer" class="newstit">McCormick Stock Gains After Q3 Earnings Beat, Raised EPS Outlook</a></h3>
          <p>摘要:McCormick & Company (NYSE:MKC) shares are trading higher after the company reported its third-quarter results and raised its full-year EPS outlook. The company registered quarterly </p>
          <P>發布時間:Tue, October 1, 2024</P>
          <span class="neutral">情緒分析: 中立</span>
        </div>
        <div class="news-card">
          <h3><a href="https://finance.yahoo.com/news/typhoon-krathon-shuts-taiwan-2-121906622.html" target="_blank" rel="noopener noreferrer" class="newstit">Typhoon Krathon Shuts Taiwan? $2.5 Trillion Stock Market</a></h3>
          <p>摘要: (Bloomberg) -- Taiwan will close its $2.5 trillion stock market as Super Typhoon Krathon approaches the island with strong winds and heavy rain.Most Read from BloombergA 7,000-Year-Old City Emerges as a Haven from Dubai? Sky-High RentsGang Violence Is Moving to the Amazon? Fast-Growing CitiesNew Rowhouses in London That Offer a Bridge to the 19th CenturyClimate Migrants Stand to Overwhelm World? MegacitiesA Housing Crisis Brews in Rwanda? Capital CityThe market will not conduct securities, c</p>
          <P>發布時間:Tue, October 1, 2024</P>
          <span class="positive">情緒分析: 中立</span>
        </div>
        <div class="news-card">
          <h3><a href="https://finance.yahoo.com/news/jobs-report-test-stock-bull-120000661.html" target="_blank" rel="noopener noreferrer" class="newstit">Jobs Report to Test Stock Bull and Fixed Income ETFs</a></h3>
          <p>摘要:All eyes are on Friday? U.S. Nonfarm Payrolls Report. </p>
          <P>發布時間:Tue, October 1, 2024</P>
          <span class="neutral">情緒分析: 正面</span>
        </div>
        <div class="news-card">
          <h3><a href="https://finance.yahoo.com/news/live/stock-market-today-dow-futures-slip-sp-500-holds-steady-with-fresh-data-on-deck-110019547.html" target="_blank" rel="noopener noreferrer" class="newstit">Stock market today: Dow futures slip, S&P 500 holds steady with fresh data on deck</a></h3>
          <p>摘要:Investors are looking to job openings and manufacturing data to provide clues to rate cuts as they digest Powell's latest comments. </p>
          <P>發布時間:Tue, October 1, 2024</P>
          <span class="negative">情緒分析: 負面</span>
        </div>


      </div>
    </div>
    <!-- 右側文字雲區域 -->
    <div class="word-cloud-container">
      <div class="word-cloud">
        <h2>文字雲</h2>
        <div class="cloud-placeholder">
          <img :src="wordCloudImage" @error="handleImageError" alt="Word Cloud Image" />
        </div>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: 'NewsAndCloud',
  data() {
    return {
      selectedNews: 'domestic',
      wordCloudImages: {
        domestic: require('@/assets/domestic-output.png'), // Ensure these paths are correct
        international: require('@/assets/international-output.png')
      }
    };
  },
  computed: {
    wordCloudImage() {
      console.log('Selected News:', this.selectedNews); // Debugging log
      console.log('Word Cloud Image:', this.wordCloudImages[this.selectedNews]); // Debugging log
      return this.wordCloudImages[this.selectedNews] || require('@/assets/fallback.jpg');
    }
  },
  methods: {
    showNews(type) {
      this.selectedNews = type;
    },
    handleImageError(event) {
      event.target.src = require('@/assets/fallback.jpg'); // Fallback image path
    }
  }
}
</script>


<style>
.news-and-cloud {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: #F5F5F5; /* Industrial-style dark background */
  margin-top: 40px; /* 與頁面上方的距離 */
}

.news-section {
  flex: 3;
  margin-right: 20px;
  color: #333; /* Light gray text for contrast */
}

.news-buttons {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 15px;
}

.news-buttons button {
  margin-right: 10px;
  padding: 8px 12px;
  border: none;
  background-color: #D3D3D3; /* Dark gray button */
  color:  #333;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}


.news-buttons button.active {
  background-color: #B0B0B0; /* Highlight active button */
}


.news-buttons button:hover {
  background-color: #A9A9A9
}

.word-cloud-container {
  flex: 1;
  align-self: flex-start;
  margin-top: 20px;
}

.word-cloud {
  margin-top: 35px;
  width: 300px;
  border: 1px solid #E0E0E0; /* Dark gray border */
  border-radius: 8px;
  padding: 80px;
  background-color: #FFFFFF; /* Slightly lighter background for contrast */
  text-align: center;
  color: #dcdcdc;
}

.cloud-placeholder img {
  max-width: 100%;
  width: 200%; /* Make the image fill the container */
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.news-card {
  background-color: #FFFFFF; /* Dark background for news cards */
  border: 1px solid #E0E0E0;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  transition: transform 0.3s ease; /* 加入過渡效果 */
}

.news-card:hover {
  transform: scale(1.05); /* 放大卡片 */
}

.news-card h3 {
  margin: 0;
  font-size: 1.5em;
  color: #333;
}


.news-card span.positive {
  color: #4CAF50; /* Soft green for positive sentiment */
}

.news-card span.negative {
  color: #F44336; /* Soft red for negative sentiment */
}

.news-card span.neutral {
  color: #FF9800; /* Blue for neutral sentiment */
}

.newstit {
  color: #333;
  text-decoration: none;
}

.newstit:hover {
  text-decoration: underline;
}

.cloud-placeholder {
  color:  #A9A9A9; /* Dim gray for placeholder text */
}
</style>