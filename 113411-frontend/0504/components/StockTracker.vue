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

      <!-- 自定義股票代碼輸入框 -->
      <div class="form-group">
        <label for="customTicker">自定義股票代碼</label><br>
        <input type="text" id="customTicker" v-model="customTicker" placeholder="輸入股票代碼"><br>
      </div>

      <!-- 目標價格輸入框 -->
      <div class="form-group">
        <label for="targetPrice">目標價格</label><br>
        <input type="number" id="targetPrice" v-model="targetPrice"><br>
      </div>

      <!-- LINE Notify Token 輸入框 -->
      <div class="form-group">
        <label for="lineNotifyToken">LINE Notify Token</label><br>
        <input type="text" id="lineNotifyToken" v-model="lineNotifyToken" placeholder="輸入您的 LINE Notify Token"><br>
        <!-- 新增 LINE Notify 連結 -->
        <a href="https://notify-bot.line.me/zh_TW/" target="_blank" class="line-notify-link">取得您的 LINE Notify Token</a>
      </div>

      <button type="submit">追蹤股價</button>
    </form>
    <p>{{ responseMessage }}</p>

    <!-- 排行選擇按鈕 -->
    <div class="ranking-buttons">
      <button
        @click="setSortType('volume')"
        :class="{ active: sortType === 'volume' }"
      >交易量排行</button>
      <button
        @click="setSortType('eps')"
        :class="{ active: sortType === 'eps' }"
      >EPS 成長率排行</button>
      <button
        @click="setSortType('changePercentage')"
        :class="{ active: sortType === 'changePercentage' }"
      >漲跌幅排行</button>
      <button
        @click="setSortType('institutionalVolume')"
        :class="{ active: sortType === 'institutionalVolume' }"
      >三大法人交易量排行</button>
    </div>

    <!-- 股票列表 -->
    <h2>推薦股票</h2>
    <table>
      <thead>
        <tr>
          <th>股票代碼</th>
          <th>公司名稱</th>
          <th>交易量</th>
          <th>股價</th>
          <th>漲跌幅</th>
          <th>EPS</th>
          <th>三大法人交易量</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in visibleStocks" :key="stock.symbol">
          <td>{{ stock.symbol }}</td>
          <td>{{ stock.name }}</td>
          <td>{{ stock.tradingVolume }}</td>
          <td>{{ stock.stockPrice.toFixed(2) }}</td>
          <td>{{ stock.changePercentage.toFixed(2) }}%</td>
          <td>{{ stock.eps }}</td>
          <td>{{ stock.institutionalVolume }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 更多按鈕 -->
    <button v-if="showMore" @click="showMoreStocks">更多</button>
  </div>
</template>


<script>
export default {
  name: 'StockTracker',
  data() {
    return {
      ticker: '',
      customTicker: '',
      targetPrice: '',
      lineNotifyToken: '',
      responseMessage: '',
      stocks: {},
      stockList: [],
      sortType: 'volume',
      visibleStocksCount: 10,
      additionalStocksCount: { volume: 0, eps: 0, changePercentage: 0, institutionalVolume: 0 }, // 每個排序類型的額外股票數量
    };
  },
  computed: {
    sortedStocks() {
      let sortedList = this.stockList.slice(); // 創建 stockList 的副本

      if (this.sortType === 'eps') {
        return sortedList.sort((a, b) => b.eps - a.eps);
      } else if (this.sortType === 'changePercentage') {
        return sortedList.sort((a, b) => b.changePercentage - a.changePercentage);
      } else if (this.sortType === 'institutionalVolume') {
        return sortedList.sort((a, b) => b.institutionalVolume - a.institutionalVolume);
      } else {
        return sortedList.sort((a, b) => b.tradingVolume - a.tradingVolume);
      }
    },
    visibleStocks() {
      const count = this.visibleStocksCount + this.additionalStocksCount[this.sortType]; // 考慮額外顯示的股票數量
      return this.sortedStocks.slice(0, count); // 返回前 count 個股票
    },
    showMore() {
      return this.sortedStocks.length > this.visibleStocksCount + this.additionalStocksCount[this.sortType]; // 檢查是否有更多股票
    },
  },
  mounted() {
    fetch('http://140.131.114.169:8082/get_stocks')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        this.stockList = data;

        // 將從後端獲取的股票資料轉換為下拉選單所需的格式
        this.stocks = data.reduce((acc, stock) => {
          acc[stock.symbol] = stock.name;
          return acc;
        }, {});
      })
      .catch(error => {
        console.error('Error fetching stock data:', error);
        this.responseMessage = '無法獲取推薦股票數據';
      });
  },
  methods: {
    trackStock() {
      const selectedTicker = this.ticker || this.customTicker;
      if (!selectedTicker || !this.targetPrice || !this.lineNotifyToken) {
        this.responseMessage = '請填寫所有必填項目';
        return;
      }

      this.responseMessage = '正在追蹤股價...';
      fetch(`http://140.131.114.169:8001/INFO/track?ticker=${selectedTicker}&target_price=${this.targetPrice}&notify_method=line&line_notify_token=${this.lineNotifyToken}`)
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
    setSortType(type) {
      this.sortType = type;
      this.visibleStocksCount = 10; // 重置可見股票數量
      this.additionalStocksCount = { volume: 0, eps: 0, changePercentage: 0, institutionalVolume: 0 }; // 重置額外股票數量
    },
    showMoreStocks() {
      this.additionalStocksCount[this.sortType] += 10; // 增加顯示的額外股票數量
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
  margin-left: 10px;
}

button:hover {
  background-color: #0056b3;
}

button.active {
  background-color: #0056b3; /* 按下後的暗色背景 */
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
  text-align: left;
}

.ranking-buttons {
  margin: 20px;
}

.line-notify-link {
  color: #007bff;
  text-decoration: underline;
  margin-top: 5px;
}

.line-notify-link:hover {
  color: #0056b3;
}
</style>
