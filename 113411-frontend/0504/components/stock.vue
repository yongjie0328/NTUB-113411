<template>
  <div>
    <h1>台股前50大公司列表</h1>

    <!-- Company List Table -->
    <table class="company-table">
      <thead>
        <tr>
          <th>公司名稱</th>
          <th>股票代號</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="company in companies" :key="company.stockCode">
          <td>
            <a href="#" @click.prevent="fetchCompanyInfo(company.stockCode)" class="company">
              {{ company.name }}
            </a>
          </td>
          <td>{{ company.stockCode }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Loading Spinner -->
    <div v-if="loading" class="loading">
      加載中...
    </div>

    <!-- Company Info -->
    <div v-if="companyInfo" class="company-info">
      <h2>{{ companyInfo.company_name }} 詳細信息</h2>
      <p><strong>股票代號:</strong> {{ companyInfo.stock_code }}</p>
      <p><strong>公司名稱:</strong> {{ companyInfo.company_name }}</p>
      <p><strong>產業類別:</strong> {{ companyInfo.industry }}</p>
      <p><strong>公司簡稱:</strong> {{ companyInfo.short_name }}</p>
      <p><strong>地址:</strong> {{ companyInfo.address }}</p>
      <p><strong>董事長:</strong> {{ companyInfo.chairman }}</p>
      <p><strong>成立時間:</strong> {{ companyInfo.founded_date }}</p>
      <p><strong>上市日期:</strong> {{ companyInfo.listed_date }}</p>
      <p><strong>普通股每股面額:</strong> {{ companyInfo.par_value_per_share }}</p>
      <p><strong>實收資本額(元):</strong> {{ companyInfo.paid_in_capital }}</p>
      <p><strong>已發行普通股數或TDR原發行股數:</strong> {{ companyInfo.total_shares_issued }}</p>
      <p><strong>編製財務報告類型:</strong> {{ companyInfo.financial_report_type }}</p>
      <p><strong>普通股盈餘分派或虧損撥補頻率:</strong> {{ companyInfo.dividend_frequency }}</p>
      <p><strong>股票過戶機構:</strong> {{ companyInfo.transfer_agency }}</p>
      <p><strong>簽證會計師事務所:</strong> {{ companyInfo.audit_firm }}</p>
      <p><strong>英文簡稱:</strong> {{ companyInfo.english_short_name }}</p>
      <p><strong>電子郵件信箱:</strong> {{ companyInfo.email }}</p>
      <p><strong>公司網址:</strong> {{ companyInfo.website }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StockForm',
  data() {
    return {
      companies: [
        { name: '臺灣水泥股份有限公司 (台泥)', stockCode: '1101' },
        { name: '統一企業股份有限公司 (統一)', stockCode: '1216' },
        { name: '台灣塑膠工業股份有限公司 (台塑)', stockCode: '1301' },
        { name: '南亞塑膠工業股份有限公司 (南亞)', stockCode: '1303' },
        { name: '台灣化學纖維股份有限公司 (台化)', stockCode: '1326' },
        { name: '亞德客國際集團 (亞德客-KY)', stockCode: '1590' },
        { name: '中國鋼鐵公司 (中鋼)', stockCode: '2002' },
        { name: '和泰汽車股份有限公司 (和泰車)', stockCode: '2207' },

        { name: '光寶科技股份有限公司 (光寶科)', stockCode: '2301' },
        { name: '聯華電子股份有限公司 (聯電)', stockCode: '2303' },
        { name: '台達電子工業股份有限公司 (台達電)', stockCode: '2308' },
        { name: '鴻海精密工業股份有限公司 (鴻海)', stockCode: '2317' },
        { name: '國巨股份有限公司 (國巨)', stockCode: '2327' },
        { name: '台灣積體電路製造股份有限公司 (台積電)', stockCode: '2330' },
        { name: '智邦科技股份有限公司 (智邦)', stockCode: '2345' },
        { name: '華碩電腦股份有限公司 (華碩)', stockCode: '2357' },

        { name: '瑞昱半導體股份有限公司 (瑞昱)', stockCode: '2379' },
        { name: '廣達電腦股份有限公司 (廣達)', stockCode: '2382' },
        { name: '研華股份有限公司 (研華)', stockCode: '2395' },
        { name: '南亞科技股份有限公司 (南亞科)', stockCode: '2408' },
        { name: '中華電信股份有限公司 (中華電)', stockCode: '2412' },
        { name: '聯發科技股份有限公司 (聯發科)', stockCode: '2454' },
        { name: '長榮航空股份有限公司 (長榮)', stockCode: '2603' },
        { name: '華南金融控股股份有限公司 (華南金)', stockCode: '2880' },

        { name: '富邦金融控股股份有限公司 (富邦金)', stockCode: '2881' },
        { name: '國泰金融控股股份有限公司 (國泰金)', stockCode: '2882' },
        { name: '凱基金融控股股份有限公司 (開發金)', stockCode: '2883' },
        { name: '玉山金融控股有限公司 (玉山金)', stockCode: '2884' },
        { name: '元大金融控股股份有限公司 (元大金)', stockCode: '2885' },
        { name: '兆豐金融控股股份有限公司 (兆豐金)', stockCode: '2886' },
        { name: '台新金融控股股份有限公司 (台新金)', stockCode: '2887' },
        { name: '永豐金融控股股份有限公司 (永豐金)', stockCode: '2890' },

        { name: '中國信託金融控股股份有限公司 (中信金)', stockCode: '2891' },
        { name: '第一金融控股股份有限公司 (第一金)', stockCode: '2892' },
        { name: '統一超商股份有限公司 (統一超)', stockCode: '2912' },
        { name: '鴻海精密工業股份有限公司 (鴻海)', stockCode: '2317' },
        { name: '大立光電股份有限公司 (大立光)', stockCode: '3008' },
        { name: '奇鋐科技股份有限公司 (奇鋐)', stockCode: '3017' },
        { name: '聯詠科技股份有限公司 (聯詠)', stockCode: '3034' },
        { name: '欣興電子股份有限公司 (欣興)', stockCode: '3037' },

        { name: '台灣大哥大股份有限公司 (台灣大)', stockCode: '3045' },
        { name: '緯創資通股份有限公司 (緯創)', stockCode: '3231' },
        { name: '世芯電子股份有限公司 (世芯-KY)', stockCode: '3661' },
        { name: '日月光投資控股股份有限公司 (日月光投控)', stockCode: '3711' },
        { name: '遠傳電信股份有限公司 (遠傳)', stockCode: '4904' },
        { name: '和碩聯合科技股份有限公司 (和碩)', stockCode: '4938' },
        { name: '中租控股股份有限公司 (中租-KY)', stockCode: '5871' },
        { name: '上海商業儲蓄銀行股份有限公司 (上海商銀)', stockCode: '5876' },

        { name: '合作金庫銀行股份有限公司 (合庫金)', stockCode: '5880' },
        { name: '台塑石化股份有限公司 (台塑化)', stockCode: '6505' },
        { name: '緯穎科技服務股份有限公司 (緯穎)', stockCode: '6669' },
       
       
       
       
        // Add more companies if needed
      ],
      companyInfo: null,
      loading: false,
    };
  },
  methods: {
    async fetchCompanyInfo(stockCode) {
      this.loading = true;
      this.companyInfo = null; // Clear previous data
      try {
        const response = await axios.get('http://140.131.114.169:8001/STOCK/data_id_info', {
          params: {
            table_name: 'sii_stock_info',
            value: stockCode,
          },
        });

        // API returns an array of arrays
        const [data] = response.data.content;

        // Map the response to the expected object format
        this.companyInfo = {
          stock_code: data[0],
          company_name: data[1],
          short_name: data[2],
          industry: data[3],
          address: data[4],
          chairman: data[5],
          founded_date: data[6],
          listed_date: data[7],
          par_value_per_share: data[8],
          paid_in_capital: data[9],
          total_shares_issued: data[10],
          financial_report_type: data[11],
          dividend_frequency: data[12],
          dividend_resolution_level: data[13],
          transfer_agency: data[14],
          audit_firm: data[15],
          english_short_name: data[16],
          email: data[17],
          website: data[18],
        };

      } catch (error) {
        console.error('Error fetching company info:', error);
        alert('無法加載公司信息');
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
h1 {
  margin-top: 60px;
  margin-bottom: 20px;
}

.company-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  margin-bottom: 50px;
}




.company-table th{
  color: blue;
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
  font-size: 20px;
}

.company-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
}

.company{
  text-align: left;
}

.company-table a {
  color: rgb(8, 31, 92); /* Set link color to black */
  text-decoration: none;
}

.company-table a:hover {
  text-decoration: underline;
}

.company-info {
  margin-top: 40px;
  padding: 20px;
  border: 1px solid #ccc;
}

.loading {
  margin-top: 20px;
  font-weight: bold;
  color: #555;
}
</style>
