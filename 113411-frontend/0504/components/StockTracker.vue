<template>
  <div class="stock-tracker">
    <h2>股票價格追蹤</h2>
    <form @submit.prevent="trackStock">
      <!-- 下拉選單 -->
      <div class="form-group">
        <label for="ticker">股票代碼</label><br>
        <select id="ticker" v-model="ticker">
          <option value="" disabled selected>選擇股票代碼</option>
          <option v-for="(name, code) in stocks" :key="code" :value="code">
            {{ code }} - {{ name }}
          </option>
        </select><br>
      </div>

      <!-- 原本的輸入框 -->
      <div class="form-group">
        <label for="customTicker">自定義股票代碼</label><br>
        <input type="text" id="customTicker" v-model="customTicker" placeholder="輸入股票代碼"><br>
      </div>

      <!-- 目標價格輸入框 -->
      <div class="form-group">
        <label for="targetPrice">目標價格</label><br>
        <input type="number" id="targetPrice" v-model="targetPrice"><br>
      </div>

      <button type="submit">追蹤股價</button>
    </form>
    <p>{{ responseMessage }}</p>
  </div>
</template>

<script>
export default {
  name: 'StockTracker',
  data() {
    return {
      ticker: '', // 下拉選單的值
      customTicker: '', // 自定義輸入框的值
      targetPrice: '',
      responseMessage: '',
      stocks: {
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
  watch: {
    // 監聽下拉選單的變化
    ticker(newVal) {
      if (newVal) {
        this.customTicker = ''; // 清空自定義輸入框
      }
    },
    // 監聽自定義輸入框的變化
    customTicker(newVal) {
      if (newVal) {
        this.ticker = ''; // 清空下拉選單
      }
    },
  },
  methods: {
    trackStock() {
      const selectedTicker = this.ticker || this.customTicker; // 使用下拉選單或自定義輸入框的值
      if (!selectedTicker) {
        this.responseMessage = '請選擇或輸入股票代碼';
        return;
      }
      
      this.responseMessage = '正在追蹤股價...';
      fetch(`http://192.168.50.15:8081/track?ticker=${selectedTicker}&target_price=${this.targetPrice}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
          }
          return response.json();
        })
        .then(data => {
          this.responseMessage = '伺服器回應：' + data.message;
        })
        .catch(error => {
          console.error('錯誤:', error);
          this.responseMessage = '錯誤：' + error.message;
        });
    },
  },
};
</script>

<style scoped>
.stock-tracker {
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

input[type="text"],
input[type="number"],
select {
  width: 30%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  margin-bottom: 10px;
}

button {
  padding: 12px 24px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>
