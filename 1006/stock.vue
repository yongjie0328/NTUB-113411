<template>
  <div>
  <!--<h1>公司列表</h1>--->

    <!-- Company List by Industry -->
    <div v-for="(companies, industry) in groupedCompanies" :key="industry">
      <h1>{{ industry }}</h1>
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
    </div>


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

       
       
       
       
        // Add more companies if needed
      ],
      companyInfo: null,
      loading: false,
    };
  },
  computed: {
    groupedCompanies() {
      return this.companies.reduce((groups, company) => {
        const industry = company.industry;
        if (!groups[industry]) {
          groups[industry] = [];
        }
        groups[industry].push(company);
        return groups;
      }, {});
    },
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
  color: rgb(24, 144, 171);
  font-size: 40px;
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
  font-size: 20px;
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
