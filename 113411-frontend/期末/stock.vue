<template>
  <div class="main-content">
    <div class="button-group">
      <button @click="showSiiInfo" :class="{ active: selectedNavItem === 'sii' }">上市公司</button>
      <button @click="showOtcInfo" :class="{ active: selectedNavItem === 'otc' }">上櫃公司</button>
    </div>
    <div v-if="isLoading">加載中...</div>
    <div v-else>
      <h2 v-if="selectedNavItem === 'sii'">上市公司資訊</h2>
      <div v-if="selectedNavItem === 'sii' && stockInfo && stockInfo.content">
        <table class="stock-table">
          <thead>
            <tr>
              <th>公司名稱</th>
              <th>股票代碼</th>
              <!-- 其他表头 -->
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in stockInfo.content" :key="index">
              <td>
                <router-link :to="{ name: 'CompanyDetails', params: { stockCode: item[0] } }">
                  {{ item[1] }}
                </router-link>
              </td>
              <td>{{ item[0] }}</td>
              <!-- 其他字段 -->
            </tr>
          </tbody>
        </table>
      </div>
      <h2 v-if="selectedNavItem === 'otc'">上櫃公司資訊</h2>
      <div v-if="selectedNavItem === 'otc' && otcInfo && otcInfo.content">
        <table class="stock-table">
          <thead>
            <tr>
              <th>公司名稱</th>
              <th>股票代碼</th>
              <!-- 其他表头 -->
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in otcInfo.content" :key="index">
              <td>
                <router-link :to="{ name: 'CompanyDetails', params: { stockCode: item[0] } }">
                  {{ item[1] }}
                </router-link>
              </td>
              <td>{{ item[0] }}</td>
              <!-- 其他字段 -->
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <router-view/>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StockForm',
  data() {
    return {
      isLoading: false,
      stockInfo: null,
      otcInfo: null,
      error: null,
      selectedNavItem: 'sii' // 初始化选中的导航项
    };
  },
  methods: {
    showSiiInfo() {
      this.selectedNavItem = 'sii';
    },
    showOtcInfo() {
      this.selectedNavItem = 'otc';
    },
    fetchData() {
      this.isLoading = true;
      axios.all([
        axios.get('http://192.168.50.174:8000/STOCK/data?table_name=sii_stock_info'), // 上市公司
        axios.get('http://192.168.50.174:8000/STOCK/data?table_name=otc_stock_info')  // 上櫃公司
      ])
      .then(axios.spread((siiResponse, otcResponse) => {
        this.stockInfo = siiResponse.data;
        this.otcInfo = otcResponse.data;
        this.isLoading = false;
      }))
      .catch(error => {
        console.error('Fetch error:', error);
        this.isLoading = false;
        this.error = "Failed to load data";
      });
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.button-group {
  margin-bottom: 20px;
  margin-top: 50px;
}

button {
  margin-right: 10px;
  padding: 8px 12px;
  border: none;
  background-color: #bed6f1;
  color: #fff;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button.active {
  background-color: #65a7ee;
  transform: scale(1.05);
}

button:hover {
  background-color: #a4c7e9;
}

.stock-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.stock-table th, .stock-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
  word-wrap: break-word;
}

.stock-table th {
  background-color: #f4f4f4;
}
</style>
