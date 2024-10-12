<template>
  <div class="container">
    <!-- Top Section: Website Introduction and Search -->
    <header class="header">
      <!-- Website Introduction -->
      <section>
        <h1>歡迎來到投資之AI應用學習</h1>
        <p>
          本平台提供上市公司的詳細資訊，有金融保險、半導體、航運、電腦及週邊設備及光電產業，助您做出明智的投資決策。
        </p>
      </section>

      <!-- Search Feature -->
      <section class="search-section">
        <h2>快速搜索公司</h2>
        <input type="text" v-model="searchQuery" placeholder="輸入公司名稱或股票代號" />
        <button @click="searchCompany">搜索</button>
      </section>
    </header>

    <!-- Main Content Section -->
    <div class="content">
      <!-- Left Sidebar: Industry Navigation -->
      <aside class="sidebar">
        <h2>產業類別</h2>
        <ul>
          <li><a href="#" @click.prevent="filterByIndustry('金融保險業')">金融保險業</a></li>
          <li><a href="#" @click.prevent="filterByIndustry('半導體業')">半導體業</a></li>
          <li><a href="#" @click.prevent="filterByIndustry('航運業')">航運業</a></li>
          <li><a href="#" @click.prevent="filterByIndustry('電腦及週邊設備業')">電腦及週邊設備業</a></li>
          <li><a href="#" @click.prevent="filterByIndustry('光電業')">光電業</a></li>
        </ul>
      </aside>

      <!-- Right Section: Company List -->
      <main class="main-content">
        <section>
          <h2>公司列表</h2>
          <table class="company-table">
            <thead>
              <tr>
                <th>公司名稱</th>
                <th>股票代號</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="company in filteredCompanies" :key="company.stockCode">
                  <td>
                  <router-link :to="{ name: 'StockPage', params: { stockCode: company.stockCode } }" class="company">
                      {{ company.name }}
                  </router-link>
                  </td>
                <td>{{ company.stockCode }}</td>
              </tr>
            </tbody>
          </table>
        </section>

       
      </main>
    </div>
  </div>
</template>

<script>


export default {
  name: 'HomePage',
  data() {
    return {
      searchQuery: "",
      companies: [
       //17 金融保險類
       { name: '新光金融控股股份有限公司 (新光金)', stockCode: '2888',industry: '金融保險業'  },
      { name: '中國信託金融控股股份有限公司 (中信金)', stockCode: '2891' ,industry: '金融保險業'},
      { name: '中華開發金融控股股份有限公司 (開發金)', stockCode: '2883',industry: '金融保險業' },
      { name: '國泰金融控股股份有限公司 (國泰金控)', stockCode: '2882',industry: '金融保險業' },
      { name: '三商美邦人壽保險股份有限公司 (三商壽)', stockCode: '2867',industry: '金融保險業' },
      { name: '玉山金融控股有限公司 (玉山金控)', stockCode: '2884',industry: '金融保險業' },
      { name: '華南金融控股股份有限公司 (華南金控)', stockCode: '2880',industry: '金融保險業' },
      { name: '永豐金融控股股份有限公司 (永豐金控)', stockCode: '2890',industry: '金融保險業' },
      { name: '臺灣中小企業銀行 (臺灣企銀)', stockCode: '2834',industry: '金融保險業' },
      { name: '元大金融控股股份有限公司 (元大金)', stockCode: '2885',industry: '金融保險業' },

     // 24 半導體業類
      { name: '聯華電子股份有限公司 (聯電)', stockCode: '2303', industry: '半導體業' },
      { name: '矽統科技股份有限公司 (矽統)', stockCode: '2363', industry: '半導體業' },
      { name: '台灣積體電路製造公司 (台積電)', stockCode: '2330' , industry: '半導體業'},
      { name: '力晶積成電子製造 (力積電)', stockCode: '6770', industry: '半導體業' },
      { name: '華邦電子股份有限公司 (華邦電)', stockCode: '2344', industry: '半導體業' },
      { name: '京元電子股份有限公司 (京元電子)', stockCode: '2449' , industry: '半導體業'},
      { name: '十銓科技股份有限公司 (十銓)', stockCode: '4967' , industry: '半導體業'},
      { name: '南亞科技股份有限公司 (南亞科)', stockCode: '2408', industry: '半導體業'},
      { name: '聯鈞光電股份有限公司 (聯鈞)', stockCode: '3450' , industry: '半導體業'},
      { name: '日月光投資控股股份有限公司 (日月光投控)', stockCode: '3711', industry: '半導體業' },

      //15 航運業類
      { name: '長榮航空股份有限公司 (長榮航)', stockCode: '2618' , industry: '航運業'},
      { name: '陽明海運股份有限公司 (陽明)', stockCode: '2609' , industry: '航運業'},
      { name: '中華航空公司 (華航)', stockCode: '2610', industry: '航運業' },
      { name: '長榮海運股份有限公司 (長榮)', stockCode: '2603', industry: '航運業' },
      { name: '萬海航運股份有限公司 (萬海)', stockCode: '2615', industry: '航運業' },
      { name: '新興航運股份有限公司 (新興)', stockCode: '2605', industry: '航運業' },
      { name: '漢翔航空工業股份有限公司 (漢翔)', stockCode: '2634' , industry: '航運業'},
      { name: '裕民航運股份有限公司 (裕民)', stockCode: '2606', industry: '航運業' },
      { name: '四維航業股份有限公司 (四維航)', stockCode: '5608', industry: '航運業' },
      { name: '慧洋海運股份有限公司 (慧洋-KY)', stockCode: '2637', industry: '航運業' },

      //25 電腦及週邊設備業類
      { name: '緯創資通股份有限公司 (緯創)', stockCode: '3231', industry: '電腦及週邊設備業' },
      { name: '宏碁股份有限公司 (宏碁)', stockCode: '2353', industry: '電腦及週邊設備業' },
      { name: '廣達電腦股份有限公司 (廣達)', stockCode: '2382', industry: '電腦及週邊設備業' },
      { name: '英業達股份有限公司 (英業達)', stockCode: '2356', industry: '電腦及週邊設備業' },
      { name: '晟銘電子科技股份有限公司 (晟銘電)', stockCode: '3013', industry: '電腦及週邊設備業' },
      { name: '仁寶電腦工業股份有限公司 (仁寶)', stockCode: '2324', industry: '電腦及週邊設備業' },
      { name: '光寶科技股份有限公司 (中鋼)', stockCode: '2301', industry: '電腦及週邊設備業' },
      { name: '昆盈企業股份有限公司 (昆盈)', stockCode: '2365', industry: '電腦及週邊設備業' },
      { name: '奇鋐科技股份有限公司 (奇鋐)', stockCode: '3017' , industry: '電腦及週邊設備業'},
      { name: '神達電腦股份有限公司 (神達)', stockCode: '3706' , industry: '電腦及週邊設備業'},

      //26 光電業類
      { name: '中環股份有限公司 (中環)', stockCode: '2323' , industry: '光電業'},
      { name: '錸德科技股份有限公司 (錸德)', stockCode: '2349', industry: '光電業' },
      { name: '佳能企業股份有限公司 (佳能)', stockCode: '2374' , industry: '光電業'},
      { name: ' 億光電子工業股份有限公司 (億光)', stockCode: '2393' , industry: '光電業'},
      { name: '國碩科技工業股份有限公司 (國碩)', stockCode: '2406', industry: '光電業' },
      { name: '友達光電股份有限公司 (友達)', stockCode: '2409' , industry: '光電業'},
      { name: '鼎元光電科技股份有限公司 (鼎元)', stockCode: '2426' , industry: '光電業'},
      { name: '銘旺科技股份有限公司 (銘旺科)', stockCode: '2429' , industry: '光電業'},
      { name: '翔耀實業股份有限公司 (翔耀)', stockCode: '2438', industry: '光電業' },
      { name: '冠西電子企業股份有限公司 (冠西電)', stockCode: '2466', industry: '光電業' },
        // 其他公司數據
      ],
      filteredCompanies: [],
      companyInfo: null,
      loading: false,
    };
  },
  methods: {
    // 公司搜索功能
    searchCompany() {
      this.filteredCompanies = this.companies.filter(
        (company) =>
          company.name.includes(this.searchQuery) ||
          company.stockCode.includes(this.searchQuery)
      );
    },

    // 按產業類別過濾公司
    filterByIndustry(industry) {
      this.filteredCompanies = this.companies.filter(
        (company) => company.industry === industry
      );
   } },
  mounted() {
    // 初次加載時顯示所有公司
    this.filteredCompanies = this.companies;
  
},
};
</script>

<style scoped>
/* 佈局樣式 */
.container-h {
display: flex;
flex-direction: column;
}

.header-h {
padding: 20px;
background-color: #4C4C4C ;
border-bottom: 1px solid #f4f1f1;
margin-top: 20px;
color: #eaeadf;
}

.search-section {
margin-top: 20px;
}

.content {
display: flex;
margin-top: 20px;
}

/* Sidebar for industry navigation */
.sidebar {
width: 30%;
padding: 20px;
border-right: 1px solid #ccc;
box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1); /* 添加陰影效果 */
}

.sidebar ul {
list-style-type: none; /* 移除前面的 . */
padding: 0;
}

.sidebar li {
margin-bottom: 30px; /* 增加產業類別之間的間距 */
}

/* Main content for company list */
.main-content {
width: 70%;
padding: 20px;
margin-bottom: 20px;
margin-top: 5px;
}

input {
margin-right: 10px;
padding: 5px;
}
h1{
  font-size: 30px;
  margin-top: 60px;
}
h2{
  font-size: 30px;
}
.company-table {
width: 100%;
border-collapse: collapse;
margin-top: 5px;
}

.company-table th, .company-table td {
border: 1px solid #ccc;
padding: 10px;
text-align: center;
font-weight: bold;
font-size: 20px;
}

.company-table th {
background-color: #f4f4f4;
font-weight: bold;
font-size: 25px;
}

.loading {
margin-top: 20px;
font-weight: bold;
color: aliceblue;
}

.company-info {
margin-top: 40px;
padding: 20px;
border: 1px solid #ccc;
}

.company {
color: #132231; /* 修改鏈接顏色 */
text-decoration: none; /* 移除下劃線 */
}

.company:hover {
color: #0056b3; /* 懸停時顏色 */
text-decoration: underline; /* 懸停時顯示下劃線 */
}
/* 產業類別鏈接顏色 */
.sidebar a {
color: #007bff; /* 修改鏈接顏色 */
text-decoration: none; /* 移除下劃線 */
font-size: 24px;
}

/* 產業類別鏈接懸停效果 */
.sidebar a:hover {
color: #0056b3; /* 懸停時顏色 */
text-decoration: underline; /* 懸停時顯示下劃線 */
}

</style>