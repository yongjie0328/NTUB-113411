<template>
  <div class="stock-layout">
   
    <div class="main-content">
      <div v-if="isLoading">加載中...</div>
      <div v-else-if="stockInfo && stockInfo.content">
        <table class="stock-table">
          <thead>
            <tr>
              <th>公司名稱</th>
              <th>公司代號</th>
              <th>產業類別</th>
              <th>公司簡稱</th>
              <th>地址</th>
              <th>董事長</th>
              <th>成立時間</th>
              <th>上櫃日期</th>
              <th>普通股每股面額</th>
              <th>實收資本額(元)</th>
              <th>已發行普通股數或TDR原發行股數</th>
              <th>編製財務報告類型</th>
              <th>普通股盈餘分派或虧損撥補頻率</th>
              <th>普通股年度(含第4季或後半年度)現金股息及紅利決議層級</th>
              <th>股票過戶機構</th>
              <th>簽證會計師事務所</th>
              <th>英文簡稱</th>
              <th>電子郵件信箱</th>
              <th>公司網址</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in stockInfo.content" :key="index">
              <td>{{ item[1] }}</td> <!-- 公司名稱 -->
              <td>{{ item[0] }}</td> <!-- 公司代號 -->
              <td>{{ item[3] }}</td> <!-- 產業類別 -->
              <td>{{ item[2] }}</td> <!-- 公司簡稱 -->
              <td>{{ item[4] }}</td> <!-- 地址 -->
              <td>{{ item[5] }}</td> <!-- 董事長 -->
              <td>{{ item[6] }}</td> <!-- 成立時間 -->
              <td>{{ item[7] }}</td> <!-- 上櫃日期 -->
              <td>{{ item[8] }}</td> <!-- 普通股每股面額 -->
              <td>{{ item[9] }}</td> <!-- 實收資本額(元) -->
              <td>{{ item[10] }}</td> <!-- 已發行普通股數或TDR原發行股數 -->
              <td>{{ item[11] }}</td> <!-- 編製財務報告類型 -->
              <td>{{ item[12] }}</td> <!-- 普通股盈餘分派或虧損撥補頻率 -->
              <td>{{ item[13] }}</td> <!-- 普通股年度現金股息及紅利決議層級 -->
              <td>{{ item[14] }}</td> <!-- 股票過戶機構 -->
              <td>{{ item[15] }}</td> <!-- 簽證會計師事務所 -->
              <td>{{ item[16] }}</td> <!-- 英文簡稱 -->
              <td>{{ item[17] }}</td> <!-- 電子郵件信箱 -->
              <td>{{ item[18] }}</td> <!-- 公司網址 -->
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>無可用數據</div>
    </div>
    
  </div>
</template>

<script>
import axios from 'axios'; // 导入 axios

export default {
  name: 'StockForm',
  data() {
    return {
      showTSM: true,
      selectedNavItem: null, // 添加一个变量来保存当前选中的导航项
      isLoading: false,
      stockInfo: null // 初始化 stockInfo 为 null
    };
  },
  methods: {
    isActive(routeName) {
      return this.selectedNavItem === routeName; // 修改为检查当前选中的导航项
    },
    showTSMInfo(routeName) {
      if (routeName === 'basic-info') {
        this.showTSM = true;
      } else {
        this.showTSM = false;
      }
      this.selectedNavItem = routeName; // 更新選中的导航项
    },
    fetchData() {
      this.isLoading = true;
      axios.get('http://172.16.66.118:8000/OTC/alldata')
  .then(response => {
    this.stockInfo = response.data; // 將返回的数据赋值给 stockInfo
    this.isLoading = false;
  })
  .catch(error => {
    console.error('Fetch error:', error);
    this.isLoading = false;
  });

    }
  },
  mounted() {
    this.fetchData(); // 在组件挂载时调用 fetchData 方法获取数据
  }
};
</script>

<style scoped>
/* 在这里添加样式，根据 selectedNavItem 的值来设置按钮的样式 */

.stock-table {
  width: 100%; /* 設定表格寬度為100% */
  border-collapse: collapse; /* 邊框合併 */
  table-layout: fixed; /* 固定表格布局 */
}

.stock-table th, .stock-table td {
  border: 1px solid #ccc;
  padding: 10px; /* 增加內距 */
  text-align: left;
  word-wrap: break-word; /* 自動換行 */
}

.stock-table th {
  background-color: #f4f4f4; /* 設置表頭背景顏色 */
}

.nav-item.active {
  background-color: #65a7ee;
  transform: scale(1.05);
}

.nav-item {
  margin-right: 10px;
  padding: 8px 12px;
  border: none;
  background-color: #bed6f1;
  color: #fff;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  text-decoration: none;
}
</style>
