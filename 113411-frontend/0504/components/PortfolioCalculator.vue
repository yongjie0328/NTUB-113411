<template>
  <div class="container">
    <h1 class="title">投資組合計算器</h1>

    <form @submit.prevent="submitForm" class="form">
      <div class="form-group">
        <label for="investmentAmount">投資金額：</label>
        <input type="number" v-model="investmentAmount" required class="input" placeholder="請輸入投資金額" />
      </div>

      <div v-for="(ticker, index) in selectedTickers" :key="index" class="form-group ticker-row">
        <label>{{ availableTickers[ticker] }} ({{ ticker }}) 投資比例 (0-1)：</label>
        <input type="number" v-model="proportions[ticker]" min="0" max="1" step="0.01" required class="input" />
        <button type="button" @click="removeTicker(ticker)" class="delete-button">×</button>
      </div>

      <div class="form-group">
        <label>選擇股票：</label>
        <select v-model="selectedTicker" @change="addTicker" class="input">
          <option v-for="(name, ticker) in availableTickers" :key="ticker" :value="ticker">
            {{ name }} ({{ ticker }})
          </option>
        </select>
      </div>

      <button type="submit" class="button">計算</button>
    </form>

    <div v-if="result" class="result-container">
      <div class="result-box">
        <h2>計算結果</h2>
        <p><strong>投資組合的風險 (波動性):</strong> {{ result.portfolio_volatility_percentage.toFixed(2) }}%</p>
        <p><strong>預期年回報率:</strong> {{ result.portfolio_return_percentage.toFixed(2) }}%</p>
        <p><strong>可能的最大損失:</strong> {{ result.potential_loss.toFixed(2) }} 元</p>
        <p><strong>預期年收益:</strong> {{ result.expected_gain.toFixed(2) }} 元</p>
        <!-- 新增 VaR 的顯示部分 -->
        <p><strong>VaR (風險價值) 百分比:</strong> {{ result.var_percentage.toFixed(2) }}%</p>
        <p><strong>VaR (風險價值) 金額:</strong> {{ result.var_amount.toFixed(2) }} 元</p>
      </div>

      <div class="analysis-grid">
        <div v-for="(details, ticker) in result.detailed_analysis" :key="ticker" class="analysis-box">
          <h3>{{ details.company_name }} ({{ ticker }})</h3>

          <h4>技術分析指標</h4>
          <p>RSI: {{ details.technical_analysis.RSI.toFixed(2) }}</p>
          <p>50 日移動平均線: {{ details.technical_analysis.MA_50.toFixed(2) }}</p>
          <p>200 日移動平均線: {{ details.technical_analysis.MA_200.toFixed(2) }}</p>
          <p>MACD: {{ details.technical_analysis.MACD.toFixed(2) }}</p>
          <p>MACD 信號線: {{ details.technical_analysis.MACD_signal.toFixed(2) }}</p>
          <p>MACD 柱狀圖: {{ details.technical_analysis.MACD_hist.toFixed(2) }}</p>
          <p>隨機震盪 %K: {{ details.technical_analysis.Stochastic_K.toFixed(2) }}</p>
          <p>隨機震盪 %D: {{ details.technical_analysis.Stochastic_D.toFixed(2) }}</p>

          <h4>財報數據</h4>
          <p>市值: {{ details.financials.market_cap }}</p>
          <p>市盈率: {{ details.financials.price_to_earnings }}</p>
          <p>收入: {{ details.financials.revenue }}</p>
          <p>毛利: {{ details.financials.gross_profit }}</p>
          <p>負債股本比: {{ details.financials.debt_to_equity }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PortfolioCalculatorForm',
  data() {
    return {
      investmentAmount: '',
      selectedTicker: '',
      selectedTickers: [],
      proportions: {},
      result: null,
      availableTickers: {
        '2888.TW': '新光金控',
        '2891.TW': '中信金控',
        '2883.TW': '開發金控',
        '2882.TW': '國泰金控',
        '2867.TW': '三商壽',
        '2884.TW': '玉山金控',
        '2880.TW': '華南金控',
        '2890.TW': '永豐金控',
        '2834.TW': '臺企銀',
        '2885.TW': '元大金控',
        '2303.TW': '聯電',
        '2363.TW': '矽統',
        '2330.TW': '台積電',
        '6770.TW': '力積電',
        '2344.TW': '華邦電',
        '2449.TW': '京元電子',
        '4967.TW': '十銓科技',
        '2408.TW': '南亞科',
        '3450.TW': '聯鈞',
        '3711.TW': '日月光投控',
        '2618.TW': '長榮航',
        '2609.TW': '陽明海運',
        '2610.TW': '華航',
        '2603.TW': '長榮海運',
        '2615.TW': '萬海航運',
        '2605.TW': '新興航運',
        '2634.TW': '漢翔',
        '2606.TW': '裕民航運',
        '5608.TW': '四維航運',
        '2637.TW': '慧洋海運',
        '3231.TW': '緯創',
        '2353.TW': '宏碁',
        '2382.TW': '廣達電腦',
        '2356.TW': '英業達',
        '3013.TW': '晟銘電',
        '2324.TW': '仁寶電腦',
        '2301.TW': '光寶科技',
        '2365.TW': '昆盈',
        '3017.TW': '奇鋐',
        '3706.TW': '神達',
        '2323.TW': '中環',
        '2349.TW': '錸德',
        '2374.TW': '佳能',
        '2393.TW': '億光',
        '2406.TW': '國碩',
        '2409.TW': '友達光電',
        '2426.TW': '鼎元',
        '2429.TW': '銘旺科',
        '2438.TW': '翔耀',
        '2466.TW': '冠西電'
      }
    };
  },
  methods: {
    addTicker() {
      if (this.selectedTicker && !this.selectedTickers.includes(this.selectedTicker)) {
        this.selectedTickers.push(this.selectedTicker);
        this.proportions[this.selectedTicker] = 0; // 初始比例為 0
      }
    },
    removeTicker(ticker) {
      this.selectedTickers = this.selectedTickers.filter(t => t !== ticker); // 移除股票代號
      delete this.proportions[ticker]; // 移除比例
    },
    async submitForm() {
      const totalProportion = Object.values(this.proportions).reduce((acc, val) => acc + val, 0);
      if (totalProportion !== 1) {
        alert("投資比例總和必須等於 1");
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:5000/calculate_portfolio', {
          tickers: this.selectedTickers,
          proportions: this.proportions,
          investment_amount: this.investmentAmount
        });

        this.result = response.data;
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
}

.button {
  background-color: #28a745;
  color: white;
  padding: 10px 15px;
  font-size: 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.button:hover {
  background-color: #218838;
}

/* 調整刪除按鈕的大小 */
.delete-button {
margin-left: 10px;
background-color: #dc3545;
width: 50px;  /* 設定固定寬度 */
height: 40px; /* 設定固定高度 */
display: flex;
align-items: center;
justify-content: center;
font-size: 20px; /* 調整字體大小 */
color: white;
border-radius: 4px;
cursor: pointer;
transition: background-color 0.3s;
padding: 0; /* 移除內邊距 */
align-self: center;
}

.delete-button:hover {
  background-color: #c82333;
}

/* 讓每個公司的技術分析顯示在單獨的格子中，並排列併排 */
.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.analysis-box {
  padding: 15px;
  background-color: #f0f8ff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h3 {
  margin-bottom: 10px;
  color: #007bff;
}

p {
  margin: 5px 0;
  font-size: 16px;
}
</style>
