<template>
  <div class="news-and-cloud">
    <div class="news-section">
      <h2>新聞區</h2>
      <!-- 添加兩個按鈕 -->
      <div class="news-buttons">
        <button :class="{ 'active': selectedNews === 'domestic' }" @click="showNews('domestic')">國內新聞</button>
        <button :class="{ 'active': selectedNews === 'international' }" @click="showNews('international')">國外新聞</button>
      </div>
      <!-- 根據 selectedNews 顯示新聞 -->
      <div v-if="selectedNews === 'domestic'">
        <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5541357" target="_blank" rel="noopener noreferrer" class="newstit">〈台股盤後〉台積電、聯發科遭殺尾盤 終場跌98點 月線收紅留長下影線</a></h3>
          <p>摘要:台股今日呈現高檔震盪，開盤一度翻黑，不過盤中再度翻紅，最高來到 20559 點，持續挑戰前高 20883 點，不過權值股較無表現，且台積電與聯發科遭殺尾盤，終場下跌 98.92 點，以 20396.6 點作收，成交量 3575.85 億元。</p>
          <P>發布時間:2024-04-30 14:15:17</P>
          <span class="positive">關鍵字: ['台股盤後', '台積電', '聯發科', '權值股', '綠能', '520行情']</span>
        </div>
        <div class="news-card">
          <h3><a href="https://news.cnyes.com/news/id/5540220" target="_blank" rel="noopener noreferrer" class="newstit">五一調查：7成上班族隨時開機待命 爆肝業前三名：科技、金融及傳播</a></h3>
          <p>摘要:yes123 求職網進行「職場爆肝壓力指數與勞動節願望調查」，結果今 (30) 日出爐，統計指出上班族七成隨時開機待命，有 94% 下班曾手機辦公，每月變相加班 13 小時。自認工作壓力較高的業種主要有：「科技資訊」、「金融保險與會計</p>
          <P>發布時間:2024-04-30 11:24:35</P>
          <span class="positive">關鍵字: ['勞動節', '人力銀行', 'yes123']</span>
        </div>
      </div>
      <div v-if="selectedNews === 'international'">
        <div class="news-card">
          <h3><a href="#" target="_blank" rel="noopener noreferrer" class="newstit">國外新聞標題</a></h3>
          <p>摘要: </p>
          <P>發布時間:</P>
          <span class="neutral">情緒分析: 中立</span>
        </div>
        <div class="news-card">
          <h3><a href="#" target="_blank" rel="noopener noreferrer" class="newstit">國外新聞標題</a></h3>
          <p>摘要: </p>
          <P>發布時間:</P>
          <span class="positive">情緒分析: 正面</span>
        </div>
        <div class="news-card">
          <h3><a href="#" target="_blank" rel="noopener noreferrer" class="newstit">國外新聞標題</a></h3>
          <p>摘要: </p>
          <P>發布時間:</P>
          <span class="negative">情緒分析: 負面</span>
        </div>
        <div class="news-card">
          <h3><a href="#" target="_blank" rel="noopener noreferrer" class="newstit">國外新聞標題</a></h3>
          <p>摘要: </p>
          <P>發布時間:</P>
          <span class="negative">情緒分析: 負面</span>
        </div>
        <div class="news-card">
          <h3><a href="#" target="_blank" rel="noopener noreferrer" class="newstit">國外新聞標題</a></h3>
          <p>摘要: </p>
          <P>發布時間:</P>
          <span class="negative">情緒分析: 負面</span>
        </div>
        <div class="news-card">
          <h3><a href="#" target="_blank" rel="noopener noreferrer" class="newstit">國外新聞標題</a></h3>
          <p>摘要: </p>
          <P>發布時間:</P>
          <span class="negative">情緒分析: 負面</span>
        </div>
      </div>
    </div>

    <!-- 右側文字雲區域 -->
    <div class="word-cloud-container">
      <div class="word-cloud">
        <h2>文字雲</h2>
        <div class="cloud-placeholder">
          <p>這裡是文字雲的範例位置。</p>
          <!-- 您可以在此嵌入文字雲組件 -->
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
      selectedNews: 'domestic', // 初始顯示國內新聞
    };
  },
  methods: {
    showNews(type) {
      this.selectedNews = type; // 設置要顯示的新聞類型
    }
  }
}
</script>

<style>
.news-and-cloud {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  height: 79vh; /* 佔滿屏幕高度 */
  overflow-y: auto; /* 垂直滾動條 */
}


.news-section {
  flex: 3; /* 新聞區域佔3個單位 */
  margin-right: 20px;
}

.news-buttons {
  display: flex;
  justify-content: flex-start; /* 左對齊按鈕 */
  margin-bottom: 15px;
}

.news-buttons button {
  margin-right: 10px;
  padding: 8px 12px;
  border: none;
  background-color: #bed6f1;
  color: #fff;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.news-buttons button.active {
  background-color: #76aee9;
}

.news-buttons button:hover {
  background-color: #76aee9;
}

.word-cloud-container {
  flex: 1; /* 文字雲部分佔1個單位 */
  display: flex;
  justify-content: center;
  align-items: center; /* 置中對齊 */
}

.word-cloud {
  width: 300px; /* 方框寬度 */
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 80px;
  text-align: center;
}

.news-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 8px;
}

.news-card h3 {
  margin: 0;
  font-size: 1.5em;
}

.news-card span.positive {
  color: green;
}

.news-card span.negative {
  color: red;
}

.news-card span.neutral {
  color: blue;
}

.cloud-placeholder {
  color: gray;
}

.newstit{
  color: black;
  text-decoration: none;
}
</style>