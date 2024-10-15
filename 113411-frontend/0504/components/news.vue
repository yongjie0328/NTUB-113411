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
        <div class="news-card" v-for="(news, index) in domesticNews" :key="index">
          <h3>
            <a :href="news[1]" target="_blank" rel="noopener noreferrer" class="newstit">{{ news[2] }}</a>
          </h3>
          <p>摘要: {{ news[3] }}</p>
          <p>關鍵字: {{ news[4] }}</p>
          <p>發布時間: {{ news[6] }}</p>
          <p>類別: {{ news[7] }}</p>
          <!-- 動態設置情緒分析的顏色 -->
          <p :class="getSentimentClass(news[9])">情緒分析: {{ news[9] }}</p>
        </div>
      </div>

      <div v-if="selectedNews === 'international'">
        <div class="news-card" v-for="(news, index) in internationalNews" :key="index">
          <h3>
            <a :href="news[1]" target="_blank" rel="noopener noreferrer" class="newstit">{{ news[2] }}</a>
          </h3>
          <p>摘要: {{ news[3] }}</p>
          <p>關鍵字: {{ news[4] }}</p>
          <!-- 動態設置情緒分析的顏色 -->
          <p :class="getSentimentClass(news[5])">情緒分析: {{ news[5] }}</p>
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
import axios from 'axios';

export default {
  name: 'NewsAndCloud',
  data() {
    return {
      selectedNews: 'domestic',
      domesticNews: [], // 用於存儲國內新聞
      internationalNews: [], // 用於存儲國外新聞
      wordCloudImages: {
        domestic: require('@/assets/tw_stock_wordcloud.png'),
        international: require('@/assets/int_stock_wordcloud.png')
      }
    };
  },
  computed: {
    wordCloudImage() {
      return this.wordCloudImages[this.selectedNews] || require('@/assets/fallback.jpg');
    }
  },
  methods: {
    showNews(type) {
      this.selectedNews = type;
    },
    fetchDomesticNews() {
      axios.get('http://140.131.114.169:8001/NEWS/data?table_name=tw_stock_news')
        .then(response => {
          this.domesticNews = response.data.content; // 假設 API 返回的數據格式為數組
        })
        .catch(error => {
          console.error('Error fetching domestic news:', error);
        });
    },
    fetchInternationalNews() {
      axios.get('http://140.131.114.169:8001/NEWS/data?table_name=int_stock_news')
        .then(response => {
          this.internationalNews = response.data.content; // 假設 API 返回的數據格式為數組
        })
        .catch(error => {
          console.error('Error fetching international news:', error);
        });
    },
    handleImageError(event) {
      event.target.src = require('@/assets/fallback.jpg');
    },
    // 根據情緒分析值返回相應的 class
    getSentimentClass(sentiment) {
      if (sentiment === '正面' || sentiment === '積極的') {
        return 'positive';
      } else if (sentiment === '負面' || sentiment === '消極的') {
        return 'negative';
      } else {
        return 'neutral';
      }
    }
  },
  mounted() {
    this.fetchDomesticNews();
    this.fetchInternationalNews();
  }
};
</script>

<style>
.news-and-cloud {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: #F5F5F5;
  margin-top: 40px;
}

.news-section {
  flex: 3;
  margin-right: 20px;
  color: #333;
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
  background-color: #D3D3D3;
  color: #333;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.news-buttons button.active {
  background-color: #B0B0B0;
}

.news-buttons button:hover {
  background-color: #A9A9A9;
}

.word-cloud-container {
  flex: 1;
  align-self: flex-start;
  margin-top: 20px;
}

.word-cloud {
  margin-top: 35px;
  width: 100%;
  max-width: 500px;  /* 調整寬度 */
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  padding: 20px;
  background-color: #FFFFFF;
  text-align: center;
  color: #dcdcdc;
}

.cloud-placeholder img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.news-card {
  background-color: #FFFFFF;
  border: 1px solid #E0E0E0;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.news-card:hover {
  transform: scale(1.05);
}

.news-card h3 {
  margin: 0;
  font-size: 1.5em;
  color: #333;
}

.positive {
  color: #4CAF50; /* 綠色，表示正面積極 */
}

.negative {
  color: #F44336; /* 紅色，表示負面消極 */
}

.neutral {
  color: #FF9800; /* 橙色，表示中性 */
}

.newstit {
  color: #333;
  text-decoration: none;
}

.newstit:hover {
  text-decoration: underline;
}

.cloud-placeholder {
  color: #A9A9A9;
}

</style>