<template>
  <div class="container-1">
    <h1 class="title">投資組合計算器</h1>

    <form @submit.prevent="submitForm" class="form">
      <div class="form-group">
        <label for="investmentAmount">投資金額：</label>
        <input type="number" v-model="investmentAmount" required class="input" placeholder="請輸入投資金額" />
      </div>

      <!-- Risk Assessment Questions -->
      <div class="form-group">
        <label>財務狀況：</label>
        <select v-model="financialStatus" required class="input">
          <option disabled value="">請選擇您的資產與負債比</option>
          <option value="1">&lt; 1</option>
          <option value="2">1 - 3</option>
          <option value="3">&gt; 3</option>
        </select>
      </div>

      <div class="form-group">
        <label>投資經驗：</label>
        <select v-model="experience" required class="input">
          <option disabled value="">請選擇您的投資經驗年數</option>
          <option value="1">無經驗</option>
          <option value="2">1 - 5 年</option>
          <option value="3">超過 5 年</option>
        </select>
      </div>

      <div class="form-group">
        <label>投資目標期限：</label>
        <select v-model="investmentGoal" required class="input">
          <option disabled value="">請選擇您的投資期限</option>
          <option value="1">少於 3 年</option>
          <option value="2">3 - 10 年</option>
          <option value="3">超過 10 年</option>
        </select>
      </div>

      <div class="form-group">
        <label>風險偏好：</label>
        <select v-model="riskPreference" required class="input">
          <option disabled value="">請選擇您能承受的最大損失</option>
          <option value="1">5% 以下</option>
          <option value="2">5% - 15%</option>
          <option value="3">超過 15%</option>
        </select>
      </div>

      <!-- 股票選擇 -->
      <div v-for="(ticker, index) in selectedTickers" :key="index" class="form-group ticker-row">
        <label>{{ availableTickers[ticker] }} ({{ ticker }}) 投資比例 (0-1)：</label>
        <input type="number" v-model="proportions[ticker]" min="0" max="1" step="0.01" required class="input" />
        <button type="button" @click="removeTicker(ticker)" class="delete-button">×</button>
      </div>

      <div class="form-group">
        <label>選擇股票：</label>
        <select v-model="selectedTicker" @change="addTicker" class="input">
          <option disabled value="">請選擇股票</option>
          <option v-for="(name, ticker) in availableTickers" :key="ticker" :value="ticker">
            {{ name }} ({{ ticker }})
          </option>
        </select>
      </div>

      <button type="submit" class="button">計算</button>
    </form>

    <!-- 結果顯示部分 -->
    <div v-if="result" class="result-container">
      <div class="result-box">
        <h2>計算結果</h2>
        <p><strong>投資組合的風險 (波動性):</strong> {{ result.portfolio_volatility_percentage.toFixed(2) }}%</p>
        <p><strong>預期年回報率:</strong> {{ result.portfolio_return_percentage.toFixed(2) }}%</p>
        <p><strong>可能的最大損失:</strong> {{ result.potential_loss.toFixed(2) }} 元</p>
        <p><strong>預期年收益:</strong> {{ result.expected_gain.toFixed(2) }} 元</p>
        <p><strong>VaR (風險價值) 百分比:</strong> {{ result.var_percentage.toFixed(2) }}%</p>
        <p><strong>VaR (風險價值) 金額:</strong> {{ result.var_amount.toFixed(2) }} 元</p>
      </div>

      <!-- 股票分析 -->
      <div v-if="result.detailed_analysis" class="analysis-section">
        <h2>您選擇的股票分析</h2>
        <div class="analysis-grid">
          <div v-for="(details, ticker) in result.detailed_analysis" :key="ticker" class="analysis-box">
            <h3>{{ details.company_name }} ({{ ticker }})</h3>
            <p><strong>目前股價:</strong> {{ details.current_price.toFixed(2) }} 元</p>
            <p>RSI: {{ details.technical_analysis.RSI.toFixed(2) }}</p>
            <p>50 日移動平均線: {{ details.technical_analysis.MA_50.toFixed(2) }}</p>
            <p>200 日移動平均線: {{ details.technical_analysis.MA_200.toFixed(2) }}</p>
            <p>MACD: {{ details.technical_analysis.MACD.toFixed(2) }}</p>
            <p>MACD 信號線: {{ details.technical_analysis.MACD_signal.toFixed(2) }}</p>
            <p>隨機震盪 %K: {{ details.technical_analysis.Stochastic_K.toFixed(2) }}</p>
            <p>隨機震盪 %D: {{ details.technical_analysis.Stochastic_D.toFixed(2) }}</p>

            <!-- 公司基本資訊 -->
            <div class="company-info">
              <h4>公司基本資訊</h4>
              <p><strong>市值:</strong> {{ formatNumber(details.financials.market_cap) }} 元</p>
              <p><strong>本益比 (P/E):</strong> {{ details.financials.price_to_earnings || '無資料' }}</p>
              <p><strong>營收:</strong> {{ formatNumber(details.financials.revenue) }} 元</p>
              <p><strong>毛利:</strong> {{ details.financials.gross_profit || '無資料' }} 元</p>
              <p><strong>債務比率:</strong> {{ details.financials.debt_to_equity || '無資料' }}</p>
              
             
            </div>
          </div>
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
      financialStatus: '',
      experience: '',
      investmentGoal: '',
      riskPreference: '',
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
    '2466.TW': '冠西電',
      },
    };
  },
  methods: {
    addTicker() {
      if (this.selectedTicker && !this.selectedTickers.includes(this.selectedTicker)) {
        this.selectedTickers.push(this.selectedTicker);
        this.proportions[this.selectedTicker] = 0;
      }
    },
    removeTicker(ticker) {
      this.selectedTickers = this.selectedTickers.filter(t => t !== ticker);
      delete this.proportions[ticker];
    },
    formatNumber(value) {
      if (!value) return '無資料';
      return new Intl.NumberFormat().format(value);
    },
    async submitForm() {
      if (!this.financialStatus || !this.experience || !this.investmentGoal || !this.riskPreference) {
        alert('請完成所有風險評估問題');
        return;
      }

      const totalProportion = Object.values(this.proportions).reduce((acc, val) => acc + parseFloat(val), 0);
      if (totalProportion !== 1) {
        alert('投資比例總和必須等於 1');
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:5000/calculate_portfolio', {
          tickers: this.selectedTickers,
          proportions: this.proportions,
          investment_amount: parseFloat(this.investmentAmount),
          financial_status: parseInt(this.financialStatus),
          experience: parseInt(this.experience),
          investment_goal: parseInt(this.investmentGoal),
          risk_preference: parseInt(this.riskPreference),
        });

        this.result = response.data; // Save API response
      } catch (error) {
        console.error('API call failed: ', error);
        alert('計算失敗，請檢查您輸入的資料是否正確，或稍後重試。');
      }
    },
  },
};
</script>


<style>
  .form-group label {
    font-size: 22px; /* 放大字體 */
    font-weight: bold; /* 設置為粗體 */
    color: #333; /* 文字顏色 */
  }

  .container-1 {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f0f0f0; /* 淺灰色背景 */
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
    font-size: 18px; /* 整體字體大小 */
    margin-top: 40px; /* 與頁面上方的距離 */
  }

  .title {
    text-align: center;
    color: #333;
    font-size: 28px;
    margin-bottom: 30px;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: 20px; /* 更大的間距以增加閱讀性 */
  }

  .form-group {
    display: flex;
    flex-direction: column;
  }

  .input {
    font-weight: 100;
    padding: 12px;
    font-size: 18px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff; /* 白色輸入框，與背景形成對比 */
    width: 100%; /* 設置寬度為 100%，讓輸入框自適應父容器 */
    max-width: 600px; /* 設置最大寬度，避免過大 */
    transition: border-color 0.3s ease;

  }

  .button {
    background-color: #505152; /* 中性色調的按鈕 */
    color: white;
    padding: 15px 20px;
    font-size: 20px;
    font-weight: bold;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    width: 100%; /* 設定按鈕寬度為100%，自適應父容器 */
    max-width: 300px; /* 設置最大寬度，避免按鈕過大 */
    transition: background-color 0.3s ease, transform 0.3s ease;
    margin: 0 auto; /* 使用 margin 置中 */
  }

  /* 按鈕的滑過效果 */
  .button:hover {
    background-color: #707172;
    transform: scale(1.05);
  }

  /* 刪除按鈕樣式 */
  .delete-button {
    margin-left: 10px;
    background-color: #d9534f;
    padding: 10px 20px; /* 長方形的大小 */
    font-size: 18px; /* 字體增大 */
    color: white;
    border-radius: 4px; /* 長方形，圓角略微調整 */
    cursor: pointer;
    align-self: center;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: background-color 0.3s;
  }

  .delete-button:hover {
    background-color: #c9302c;
  }

  /* 結果區域 */
  .result-container {
    margin-top: 30px;
    background-color: #e9ecef;
    padding: 20px;
    border-radius: 8px;
  }

  .result-box {
    margin-bottom: 20px;
  }

  .analysis-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
  }

  .analysis-box {
    padding: 15px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  }
</style>