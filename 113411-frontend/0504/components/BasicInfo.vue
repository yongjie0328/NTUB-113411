<template>
  <div class="stock-layout">
   
    <div class="main-content">
      <h2 v-if="company">{{ company.name }} 詳細信息</h2>
      <div v-if="isLoading">加載中...</div>
      <div v-else-if="company">
        <table class="company-table">
          <thead>
            <tr>
              <th>公司名稱</th>
              <th>股票代碼</th>
              <th>產業類別</th>
              <th>公司簡稱</th>
              <th>地址</th>
              <th>董事長</th>
              <th>成立時間</th>
              <th>上市日期</th>
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
            <tr>
              <td>{{ company.name }}</td>
              <td>{{ company.stockCode }}</td>
              <td>{{ company.industry }}</td>
              <td>{{ company.shortName }}</td>
              <td>{{ company.address }}</td>
              <td>{{ company.chairman }}</td>
              <td>{{ company.foundedDate }}</td>
              <td>{{ company.listedDate }}</td>
              <td>{{ company.parValuePerShare }}</td>
              <td>{{ company.paidInCapital }}</td>
              <td>{{ company.totalSharesIssued }}</td>
              <td>{{ company.financialReportType }}</td>
              <td>{{ company.dividendFrequency }}</td>
              <td>{{ company.dividendResolutionLevel }}</td>
              <td>{{ company.transferAgency }}</td>
              <td>{{ company.auditFirm }}</td>
              <td>{{ company.englishShortName }}</td>
              <td>{{ company.email }}</td>
              <td>{{ company.website }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>未找到公司信息</p>
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
      isLoading: false,
      company: null,
      error: null,
      selectedNavItem: 'basic-info' // 初始化选中的导航项
    };
  },
  methods: {
    fetchCompanyDetails() {
      const stockCode = this.$route.params.stockCode;  // 从路由参数获取股票代码
      this.isLoading = true;
      axios.get(`http://172.16.66.118:8000/STOCK/data?table_name=sii_stock_info&stockCode=${stockCode}`)
        .then(response => {
          console.log(response.data); // 打印API返回的数据
          this.company = response.data.content[0]; // 假设返回的数据在 content 数组中
          this.isLoading = false;
        })
        .catch(error => {
          console.error('Fetch error:', error);
          this.error = 'Unable to fetch data';
          this.isLoading = false;
        });
    },
    isActive(routeName) {
      return this.selectedNavItem === routeName;
    },
    showTSMInfo(routeName) {
      this.selectedNavItem = routeName;
    }
  },
  mounted() {
    this.fetchCompanyDetails();
  }
};
</script>



<style scoped>
.stock-layout {
  display: flex;
}

.sidebar {
  width: 200px;
  margin-right: 20px;
}

.main-content {
  flex: 1;
}

.nav-item.active {
  background-color: #65a7ee;
  transform: scale(1.05);
}

.nav-item {
  display: block;
  margin-bottom: 10px;
  padding: 8px 12px;
  border: none;
  background-color: #bed6f1;
  color: #fff;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  text-decoration: none;
}

.nav-item:hover {
  background-color: #a4c7e9;
}

.company-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.company-table th, .company-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
  word-wrap: break-word;
}

.company-table th {
  background-color: #f4f4f4;
}
</style>


