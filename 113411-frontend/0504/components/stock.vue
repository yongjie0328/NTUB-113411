<template>
  <div class="company-details-container">
    <!-- Company Information Section -->
    <div v-if="companyInfo" class="company-info">
      <h2>
        <span class="company-name">
          {{ companyInfo.company_name }}
          <!-- 添加收藏星號 -->
          <button @click="toggleFavorite" class="favorite-button">
            <span v-if="isFavorite">&#9733;</span> <!-- 已收藏的星號 -->
            <span v-else>&#9734;</span> <!-- 未收藏的星號 -->
          </button>
        </span>
      </h2>
      <p><strong>股票代號:</strong> {{ companyInfo[0]}}</p>
      <p><strong>公司名稱:</strong> {{ companyInfo[1] }}</p>
      <p><strong>公司簡稱:</strong> {{ companyInfo[2] }}</p>
      <p><strong>產業類別:</strong> {{ companyInfo[3] }}</p>
      <p><strong>地址:</strong> {{ companyInfo[4] }}</p>
      <p><strong>董事長:</strong> {{ companyInfo[5] }}</p>
      <p><strong>成立時間:</strong> {{ companyInfo[6] }}</p>
      <p><strong>上市日期:</strong> {{ companyInfo[7] }}</p>
      <p><strong>普通股每股面額:</strong> {{ companyInfo[8] }}</p>
      <p><strong>實收資本額(元):</strong> {{ companyInfo[9] }}</p>
      <p><strong>已發行普通股數或TDR原發行股數:</strong> {{ companyInfo[10]}}</p>
      <p><strong>公司網址:</strong> <a :href="companyInfo[18]" target="_blank">{{ companyInfo[18]}}</a></p>
    </div>

    <!-- Historical Stock Price Section -->
    <div v-if="historicalData" class="historical-data">
      <h2>{{ companyInfo[1] }} 歷史股價</h2>
      <table class="price-table">
        <thead>
          <tr>
            <th>日期</th>
            <th>開盤價</th>
            <th>收盤價</th>
            <th>最高價</th>
            <th>最低價</th>
            <th>漲跌幅</th>
            <th>成交量</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in historicalData" :key="data[0]">
            <td>{{ data[2] }}</td> <!-- 日期 -->
            <td>{{ data[5] }}</td> <!-- 開盤價 -->
            <td>{{ data[8] }}</td> <!-- 收盤價 -->
            <td>{{ data[6] }}</td> <!-- 最高價 -->
            <td>{{ data[7] }}</td> <!-- 最低價 -->
            <td>{{ data[9] }}</td> <!-- 漲跌幅 -->
            <td>{{ data[3] }}</td> <!-- 成交量 -->
          </tr>
        </tbody>
      </table>
    </div>

 <!-- Technical Analysis Section -->
 <div v-if="companyInfo" class="technical-analysis">
      <h2>{{ companyInfo.company_name }} 技術分析</h2>
      <iframe :src="technicalAnalysisUrl" class="technical-chart-iframe"></iframe>
    </div>
    
    <!-- Technical Analysis Section -->
    <div class="company-details-container">
    <!-- Financial Analysis Section -->
    <div v-if="financialData" class="financial-analysis">
      <h2 class="financial-analysis-title">{{ companyInfo[1] }} 財務分析</h2>
      <div class="financial-table-container">
        <table class="financial-table">
          <thead>
            <tr>
              <th colspan="2">償債能力</th>
              <th colspan="2">經營能力</th>
              <th colspan="2">獲利能力</th>
            </tr>
          </thead>
          <tbody>
            <!-- 償債能力 -->
            <tr>
              <td><strong>流動比率</strong></td>
              <td>{{ financialData[2] }}%</td>
              <td><strong>應收款項週轉率</strong></td>
              <td>{{ financialData[5] }}次</td>
              <td><strong>資產報酬率</strong></td>
              <td>{{ financialData[11] }}%</td>
            </tr>
            <tr>
              <td><strong>速動比率</strong></td>
              <td>{{ financialData[3] }}%</td>
              <td><strong>平均收現日數</strong></td>
              <td>{{ financialData[6] }}天</td>
              <td><strong>權益報酬率</strong></td>
              <td>{{ financialData[12] }}%</td>
            </tr>
            <tr>
              <td><strong>利息保障倍數</strong></td>
              <td>{{ financialData[4] }}</td>
              <td><strong>存貨週轉率</strong></td>
              <td>{{ financialData[7] }}次</td>
              <td><strong>稅前純益佔實收資本比率</strong></td>
              <td>{{ financialData[13] }}%</td>
            </tr>

            <!-- 經營能力 -->
            <tr>
              <td></td>
              <td></td>
              <td><strong>不動產、廠房及設備週轉率</strong></td>
              <td>{{ financialData[9] }}次</td>
              <td><strong>純益率</strong></td>
              <td>{{ financialData[14] }}%</td>
            </tr>
            <tr>
              <td></td>
              <td></td>
              <td><strong>總資產週轉率</strong></td>
              <td>{{ financialData[10] }}次</td>
              <td><strong>每股盈餘</strong></td>
              <td>{{ financialData[15] }}元</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'CompanyDetails',
  data() {
    return {
      companyInfo: null,
      historicalData: null,
      financialData: null,
      technicalAnalysisUrl: '', // 用于存储技术分析图表的 URL
      loading: true,
      isFavorite: false, // 用于跟踪当前股票是否被收藏
    };
  },
  methods: {
    async fetchCompanyDetails(stockCode) {
      this.loading = true;

      try {
        // Fetch company info
        const companyResponse = await axios.get('http://140.131.114.169:8001/STOCK/data_id_info', {
          params: {
            table_name: 'sii_stock_info',
            value: stockCode,
          },
        });
        if (companyResponse.data && companyResponse.data.content && companyResponse.data.content.length > 0) {
          this.companyInfo = companyResponse.data.content[0];
        } else {
          alert('公司資料不存在');
        }

        // Fetch historical stock price data
        const historicalResponse = await axios.get('http://140.131.114.169:8001/STOCK/data_price_info', {
          params: {
            table_name: 'sii_stock_price',
            value: stockCode,
          },
        });
        this.historicalData = historicalResponse.data.content;

        // Fetch financial analysis data
        const financialResponse = await axios.get('http://140.131.114.169:8001/STOCK/data_financial_analysis_info', {
          params: {
            table_name: 'sii_stock_financial_analysis',
            value: stockCode,
          },
        });
        this.financialData = financialResponse.data.content[0];
      } catch (error) {
        console.error('Error fetching company details:', error);
        alert('無法加載公司信息');
      }
    },

    // 切換收藏狀態
    toggleFavorite() {
      const stockCode = this.companyInfo[0];
      if (this.isFavorite) {
        this.removeFromFavorites(stockCode);
      } else {
        this.addToFavorites(stockCode);
      }
      this.isFavorite = !this.isFavorite; 
      this.updateNavbarFavorites(); // 同步更新導航欄的收藏列表// 反轉星星的狀態，不需要重整頁面
    },

    // 添加到收藏
    addToFavorites(stockCode) {
      let favorites = JSON.parse(localStorage.getItem('favoriteStocks')) || [];
      if (!favorites.includes(stockCode)) {
        favorites.push(stockCode);
        localStorage.setItem('favoriteStocks', JSON.stringify(favorites));
      }
    },

    // 從收藏中移除
    removeFromFavorites(stockCode) {
      let favorites = JSON.parse(localStorage.getItem('favoriteStocks')) || [];
      favorites = favorites.filter(code => code !== stockCode);
      localStorage.setItem('favoriteStocks', JSON.stringify(favorites));
    },
     // 檢查股票是否被收藏
     checkIfFavorite(stockCode) {
      let favorites = JSON.parse(localStorage.getItem('favoriteStocks')) || [];
      return favorites.includes(stockCode);
    },

    // 更新導航欄收藏列表
    updateNavbarFavorites() {
      window.dispatchEvent(new Event('storage'));  // 通知導航欄更新
    }
  },
  watch: {
    '$route.params.stockCode': {
      immediate: true,
      handler(newStockCode) {
        this.isFavorite = this.$route.params.isFavorite; // 立即更新星星狀態
        this.fetchCompanyDetails(newStockCode); // 加载新股票資料
      }
    },
  },
  mounted() {
    this.isFavorite = this.$route.params.isFavorite; // 直接設置是否為收藏
    this.fetchCompanyDetails(this.$route.params.stockCode); // 加载公司資料
  },
};
</script>




<style scoped>
.company-details-container {
  padding: 20px;
}

.loading {
  text-align: center;
  font-size: 18px;
  margin-top: 20px;
}

.company-info, .historical-data, .technical-analysis, .financial-analysis {
  margin-top: 40px;
  padding: 20px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  text-align: center;
}

.price-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.price-table th, .price-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
}

.price-table th {
  background-color: #f4f4f4;
}

.technical-chart-iframe {
  width: 100%;
  height: 400px;
  border: none;
}

.favorite-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 30px;
  color: #ffcc00; /* 金色星号 */
}
.favorite-button:hover {
  color: #ffaa00; /* 悬停时的颜色 */
}

.financial-table-container {
  display: flex;
  justify-content: center;
  margin: 20px auto;
  width: 90%; /* 設置寬度為父容器的90% */
  animation: fadeIn 1.5s ease-in-out;
}

.financial-table {
  width: 100%;
  max-width: 1200px;
  border-collapse: collapse;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.financial-table th, 
.financial-table td {
  border: 1px solid #ccc;
  padding: 15px 20px;
  text-align: center;
  white-space: nowrap;
  transition: background-color 0.3s ease, color 0.3s ease; /* 背景色和字體顏色過渡效果 */
}

.financial-table th {
  background-color: #f4f4f4;
  font-weight: bold;
  font-size: 18px;
}

.financial-table td {
  font-size: 16px;
}

.nowrap {
  white-space: nowrap;
}

.financial-table th {
  background-color: #f4f4f4;
  font-weight: bold;
  font-size: 18px;
}

.financial-table td {
  font-size: 16px;
}

</style>
