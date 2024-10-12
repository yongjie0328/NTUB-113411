<template>
  <div class="container">
    <h1 class="title">投資組合計算器</h1>

    <!-- Risk Assessment Section -->
    <div class="risk-assessment-container">
      <!-- Risk Assessment Form (Left Side) -->
      <form @submit.prevent="submitRiskAssessment" class="form risk-assessment-form">
        <!-- Financial Status -->
        <div class="form-group">
          <label>您的收入穩定性如何？</label>
          <div class="radio-group">
            <label><input type="radio" v-model="financialStatus" value="1" required /> 不穩定，收入可能隨時減少</label>
            <label><input type="radio" v-model="financialStatus" value="2" required /> 偶爾波動，收入大致穩定</label>
            <label><input type="radio" v-model="financialStatus" value="3" required /> 非常穩定，幾乎沒有波動</label>
          </div>
        </div>

        <!-- Experience -->
        <div class="form-group">
          <label>您每月的收入與支出情況如何？</label>
          <div class="radio-group">
            <label><input type="radio" v-model="experience" value="1" required /> 每月幾乎無結餘，甚至入不敷出</label>
            <label><input type="radio" v-model="experience" value="2" required /> 有少量結餘，能存下一些錢</label>
            <label><input type="radio" v-model="experience" value="3" required /> 每月有較大結餘，存款穩定增加</label>
          </div>
        </div>

        <!-- Investment Goal -->
        <div class="form-group">
          <label>投資目標期限：</label>
          <div class="radio-group">
            <label><input type="radio" v-model="investmentGoal" value="1" required /> 少於 3 年</label>
            <label><input type="radio" v-model="investmentGoal" value="2" required /> 3 - 10 年</label>
            <label><input type="radio" v-model="investmentGoal" value="3" required /> 超過 10 年</label>
          </div>
        </div>

        <!-- Risk Preference -->
        <div class="form-group">
          <label>風險偏好：</label>
          <div class="radio-group">
            <label><input type="radio" v-model="riskPreference" value="1" required /> 5% 以下</label>
            <label><input type="radio" v-model="riskPreference" value="2" required /> 5% - 15%</label>
            <label><input type="radio" v-model="riskPreference" value="3" required /> 超過 15%</label>
          </div>
        </div>

        <button type="submit" class="button">提交風險評估</button>
      </form>

      <!-- Result Display (Right Side) -->
      <div v-if="riskAssessmentResult" class="result-container">
        <div class="result-box">
          <h2>風險評估結果</h2>
          <p><strong>您的風險承受度分數是:</strong> {{ riskAssessmentResult.totalScore }}</p>
          <p><strong>資產配置建議:</strong> {{ riskAssessmentResult.allocation }}</p>
        </div>
      </div>
    </div>

    <!-- Investment Details Section with Results Side by Side -->
    <div class="investment-container">
      <!-- Investment Form (Left Side) -->
      <div class="investment-form">
        <form @submit.prevent="submitInvestmentDetails" class="form investment-details-form">
          <div class="form-group">
            <label for="investmentAmount">投資金額：</label>
            <input type="number" v-model="investmentAmount" required class="input" placeholder="請輸入投資金額" />
          </div>

          <!-- 股票選擇 -->
          <div v-for="(ticker, index) in selectedTickers" :key="index" class="form-group ticker-row">
            <label>{{ availableTickers[ticker] }} ({{ ticker }}) 投資比例 (0-1)：</label>
            <div class="ticker-input-group">
              <input type="number" v-model="proportions[ticker]" min="0" max="1" step="0.01" required class="input" />
              <button type="button" @click="removeTicker(ticker)" class="delete-button">×</button>
            </div>
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

          <button type="submit" class="button">提交投資組合</button>
        </form>
      </div>

      <!-- Investment Calculation Result and Stock Details (Right Side) -->
      <div class="result-container">
        <div v-if="investmentResult && Object.keys(investmentResult).length > 0" class="result-box">
          <h2>投資計算結果</h2>
          <p><strong>投資組合的風險 (波動性):</strong> {{ formatNumber(investmentResult.portfolio_volatility_percentage) }}%</p>
          <p><strong>預期年回報率:</strong> {{ formatNumber(investmentResult.portfolio_return_percentage) }}%</p>
          <p><strong>可能的最大損失:</strong> {{ formatNumber(investmentResult.potential_loss) }} 元</p>
          <p><strong>預期年收益:</strong> {{ formatNumber(investmentResult.expected_gain) }} 元</p>
          <p><strong>VaR (風險價值) 百分比:</strong> {{ formatNumber(investmentResult.var_percentage) }}%</p>
          <p><strong>VaR (風險價值) 金額:</strong> {{ formatNumber(investmentResult.var_amount) }} 元</p>
        </div>

        <!-- Stock Details -->
        <div v-if="investmentResult.detailed_analysis && Object.keys(investmentResult.detailed_analysis).length > 0">
          <div v-for="(analysis, ticker) in investmentResult.detailed_analysis" :key="ticker" class="stock-details">
            <h3>{{ analysis.company_name }} ({{ ticker }})</h3>
            <p><strong>即時股價:</strong> {{ formatNumber(analysis.current_price) }}</p>
            <h4>技術分析</h4>
            <ul class="no-bullets">
              <li><strong>RSI:</strong> {{ formatNumber(analysis.technical_analysis.RSI) }}</li>
              <li><strong>MA 50:</strong> {{ formatNumber(analysis.technical_analysis.MA_50) }}</li>
              <li><strong>MA 200:</strong> {{ formatNumber(analysis.technical_analysis.MA_200) }}</li>
              <li><strong>MACD:</strong> {{ formatNumber(analysis.technical_analysis.MACD) }}</li>
              <li><strong>MACD Signal:</strong> {{ formatNumber(analysis.technical_analysis.MACD_signal) }}</li>
              <li><strong>Stochastic K:</strong> {{ formatNumber(analysis.technical_analysis.Stochastic_K) }}</li>
              <li><strong>Stochastic D:</strong> {{ formatNumber(analysis.technical_analysis.Stochastic_D) }}</li>
            </ul>
            <h4>財務數據</h4>
            <ul class="no-bullets">
              <li><strong>市值:</strong> {{ formatNumber(analysis.financials.market_cap) }}</li>
              <li><strong>本益比:</strong> {{ formatNumber(analysis.financials.price_to_earnings) }}</li>
              <li><strong>營收:</strong> {{ formatNumber(analysis.financials.revenue) }}</li>
              <li><strong>毛利:</strong> {{ formatNumber(analysis.financials.gross_profit) }}</li>
              <li><strong>負債比:</strong> {{ formatNumber(analysis.financials.debt_to_equity) }}</li>
            </ul>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PortfolioCalculatorForm',
  data() {
    return {
      investmentResult: {
        portfolio_volatility_percentage: 0,
        portfolio_return_percentage: 0,
        potential_loss: 0,
        expected_gain: 0,
        var_percentage: 0,
        var_amount: 0,
        detailed_analysis: {}
      },
      investmentAmount: '',
      selectedTicker: '',
      selectedTickers: [],
      proportions: {},
      riskAssessmentResult: null,
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
        '2466.TW': '冠西電'
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
    formatNumber(value) {
      return (value !== undefined && value !== null) ? Number(value).toFixed(2) : 'N/A';
    },
    removeTicker(ticker) {
      this.selectedTickers = this.selectedTickers.filter(t => t !== ticker);
      delete this.proportions[ticker];
    },
    async submitRiskAssessment() {
      if (!this.financialStatus || !this.experience || !this.investmentGoal || !this.riskPreference) {
        alert('請完成所有風險評估問題');
        return;
      }
      const totalScore = parseInt(this.financialStatus) + parseInt(this.experience) + parseInt(this.investmentGoal) + parseInt(this.riskPreference);
      let allocation = '';
      if (totalScore >= 16) {
        allocation = '建議高風險投資，股票佔比 80%，儲蓄佔比 20%。';
      } else if (totalScore >= 8 && totalScore < 16) {
        allocation = '建議中等風險投資，股票佔比 60%，儲蓄佔比 40%。';
      } else {
        allocation = '建議低風險投資，股票佔比 40%，儲蓄佔比 60%。';
      }
      this.riskAssessmentResult = { totalScore, allocation };
    },
    async submitInvestmentDetails() {
      console.log('submitInvestmentDetails method called');
      console.log('Selected Tickers:', this.selectedTickers);
      console.log('Proportions:', this.proportions);
      console.log('Investment Amount:', this.investmentAmount);

      const totalProportion = Object.values(this.proportions).reduce((acc, val) => acc + parseFloat(val), 0);
      if (totalProportion !== 1) {
        alert('投資比例總和必須等於 1');
        return;
      }

      // Construct the investmentDetails object for submission
      const investmentDetails = {
        investment_amount: this.investmentAmount,  // Correct field name
        tickers: this.selectedTickers,
        proportions: this.proportions,
      };

      try {
        const response = await fetch('http://127.0.0.1:5000/calculate_portfolio', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(investmentDetails)
        });

        if (!response.ok) {
          throw new Error('Network response was not ok.');
        }

        const data = await response.json();
        console.log('API response:', data);
        this.investmentResult = data; // Update the result data
      } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
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

  .container {
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
    margin-top: 50px;
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
    font-size: 20px;
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

  .no-bullets {
    list-style-type: none;
    padding: 0;
  }

  .ticker-input-group {
    display: flex;
    align-items: center;
  }
</style>
