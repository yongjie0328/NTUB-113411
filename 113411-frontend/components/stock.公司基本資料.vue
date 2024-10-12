<template>
  <div class="company-details-container">
    <!-- Loading Spinner -->
    <div v-if="loading" class="loading">
      加載中...
    </div>

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
      <p><strong>股票代號:</strong> {{ companyInfo.stock_code }}</p>
      <p><strong>公司名稱:</strong> {{ companyInfo.company_name }}</p>
      <p><strong>產業類別:</strong> {{ companyInfo.industry }}</p>
      <p><strong>地址:</strong> {{ companyInfo.address }}</p>
      <p><strong>董事長:</strong> {{ companyInfo.chairman }}</p>
      <p><strong>成立時間:</strong> {{ companyInfo.founded_date }}</p>
      <p><strong>上市日期:</strong> {{ companyInfo.listed_date }}</p>
      <p><strong>普通股每股面額:</strong> {{ companyInfo.par_value_per_share }}</p>
      <p><strong>實收資本額(元):</strong> {{ companyInfo.paid_in_capital }}</p>
      <p><strong>已發行普通股數或TDR原發行股數:</strong> {{ companyInfo.total_shares_issued }}</p>
      <p><strong>公司網址:</strong> <a :href="companyInfo.website" target="_blank">{{ companyInfo.website }}</a></p>
    </div>

    <!-- Historical Stock Price Section -->
    <div v-if="historicalData" class="historical-data">
      <h2>{{ companyInfo.company_name }} 歷史股價</h2>
      <table class="price-table">
        <thead>
          <tr>
            <th>日期</th>
            <th>開盤價</th>
            <th>收盤價</th>
            <th>最高價</th>
            <th>最低價</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in historicalData" :key="data.date">
            <td>{{ data.date }}</td>
            <td>{{ data.open }}</td>
            <td>{{ data.close }}</td>
            <td>{{ data.high }}</td>
            <td>{{ data.low }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Technical Analysis Section -->
    <div v-if="companyInfo" class="technical-analysis">
      <h2>{{ companyInfo.company_name }} 技術分析</h2>
      <iframe :src="technicalAnalysisUrl" class="technical-chart-iframe"></iframe>
    </div>

    <!-- Financial Analysis Section -->
    <div v-if="financialData" class="financial-analysis">
      <h2>{{ companyInfo.company_name }} 財務分析</h2>
      <p><strong>總營收:</strong> {{ financialData.revenue }}</p>
      <p><strong>淨利:</strong> {{ financialData.netIncome }}</p>
      <p><strong>毛利率:</strong> {{ financialData.grossMargin }}%</p>
      <p><strong>每股盈餘 (EPS):</strong> {{ financialData.eps }}</p>
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
    async fetchCompanyDetails() {
      const stockCode = this.$route.params.stockCode;
      this.loading = true;

      try {
        // Fetch company info
        const companyResponse = await axios.get('http://127.0.0.1:8000/STOCK/data_id_info', {
          params: {
            value: stockCode,
          },
        });
        this.companyInfo = companyResponse.data.content[0];

        // Fetch historical stock price data
        const historicalResponse = await axios.get(`http://127.0.0.1:8000/historical/${stockCode}`);
        this.historicalData = historicalResponse.data;

        // Set technical analysis URL
        this.technicalAnalysisUrl = `http://127.0.0.1:8000/technical_analysis/${stockCode}`;

        // Fetch financial analysis data
        const financialResponse = await axios.get(`http://127.0.0.1:8000/financial/${stockCode}`);
        this.financialData = financialResponse.data;

        // 初始化收藏狀態
        this.isFavorite = this.checkIfFavorite(stockCode);
      } catch (error) {
        console.error('Error fetching company details:', error);
        alert('無法加載公司信息');
      } finally {
        this.loading = false;
      }
    },
    toggleFavorite() {
      const stockCode = this.companyInfo.stock_code;
      if (this.isFavorite) {
        // 移除收藏
        this.removeFromFavorites(stockCode);
      } else {
        // 添加到收藏
        this.addToFavorites(stockCode);
      }
      this.isFavorite = !this.isFavorite;
    },
    addToFavorites(stockCode) {
      let favorites = JSON.parse(localStorage.getItem('favoriteStocks')) || [];
      favorites.push(stockCode);
      localStorage.setItem('favoriteStocks', JSON.stringify(favorites));
    },
    removeFromFavorites(stockCode) {
      let favorites = JSON.parse(localStorage.getItem('favoriteStocks')) || [];
      favorites = favorites.filter(code => code !== stockCode);
      localStorage.setItem('favoriteStocks', JSON.stringify(favorites));
    },
    checkIfFavorite(stockCode) {
      let favorites = JSON.parse(localStorage.getItem('favoriteStocks')) || [];
      return favorites.includes(stockCode);
    },
  },
  mounted() {
    this.fetchCompanyDetails();
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
</style>
