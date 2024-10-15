<template>
  <div class="container">
    <h1 class="title">股票預測結果</h1>
    <div class="input-group">
      <select v-model="selectedTicker" class="ticker-select" @change="clearPreviousData('dropdown')">
        <option value="">選擇股票</option>
        <option v-for="(name, code) in stockList" :key="code" :value="code">
          {{ name }} ({{ code }})
        </option>
      </select>
      <input v-model="customTicker" class="ticker-input" placeholder="或手動輸入股票代碼" @input="clearPreviousData('input')">
      <button @click="getPrediction" class="predict-button">獲取預測</button>
    </div>
    <div v-if="currentPrice" class="current-price">
      <h2>目前股價: ${{ currentPrice.toFixed(2) }}</h2>
    </div>
    <table v-if="predictions.length > 0" class="prediction-table">
      <thead>
        <tr>
          <th>日期</th>
          <th>預測價格</th>
          <th>下限</th>
          <th>上限</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prediction in predictions" :key="prediction.ds">
          <td>{{ formatDate(prediction.ds) }}</td>
          <td>{{ prediction.yhat.toFixed(2) }}</td>
          <td>{{ prediction.yhat_lower.toFixed(2) }}</td>
          <td>{{ prediction.yhat_upper.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
    <div v-if="imageUrl" class="chart-container">
      <h2>股票預測圖像</h2>
      <img :src="imageUrl" alt="Stock Prediction Chart" class="prediction-image" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'StockPredictionForm',
  data() {
    return {
      selectedTicker: '',
      customTicker: '',
      currentPrice: null,
      predictions: [],
      imageUrl: '',
      stockList: {
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
    clearPreviousData(source) {
      if (source === 'dropdown') {
        this.customTicker = ''; // 清空输入框
      } else if (source === 'input') {
        this.selectedTicker = ''; // 清空下拉框
      }
      this.currentPrice = null;
      this.predictions = [];
      this.imageUrl = '';
    },
    async getPrediction() {
      let ticker = this.selectedTicker || this.customTicker;

      // 如果用户没有输入后缀，自动添加 .TW
      if (ticker && !ticker.endsWith('.TW')) {
        ticker += '.TW';
      }

      if (!ticker) {
        alert('請選擇股票或輸入股票代碼');
        return;
      }

      try {
        const responses = await Promise.all([
          fetch(`http:///140.131.114.169:5000/current-price?ticker=${ticker}`),
          fetch(`http:///140.131.114.169:5000/predict?ticker=${ticker}&days=90`),
          fetch(`http:///140.131.114.169:5000/predict-image?ticker=${ticker}&days=90`)
        ]);

        const [priceResponse, predictionResponse, imageResponse] = responses;

        if (!priceResponse.ok || !predictionResponse.ok || !imageResponse.ok) {
          throw new Error('Network response was not ok.');
        }

        const priceData = await priceResponse.json();
        const predictions = await predictionResponse.json();
        const imageBlob = await imageResponse.blob();

        this.currentPrice = priceData.currentPrice;
        this.predictions = predictions;
        this.imageUrl = URL.createObjectURL(imageBlob);

      } catch (error) {
        console.error('Error fetching prediction or image:', error);
        alert(`錯誤: ${error.message}`);
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return `${date.getFullYear() - 1911}/${date.getMonth() + 1}/${date.getDate()}`;
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1500px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  font-size: 24px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.input-group {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.ticker-select, .ticker-input {
  width: 40%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
}

.predict-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #54546c;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.predict-button:hover {
  background-color: #858599;
}

.current-price {
  text-align: center;
  font-size: 1.5em;
  margin: 20px 0;
  color: #333;
  font-size: 20px;
}

.prediction-image {
  max-width: 100%;
  height: auto;
  margin-top: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

h2 {
  font-size: 30px;
}
</style>
