<template>
  <div>
    <div class="sidebar">
      <!-- 按钮 -->
      <button class="nav-item" :class="{ 'active': selectedNavItem === 'basic-info' }"
        @click="showTSMInfo('basic-info')">基本資料</button>
      <button class="nav-item" :class="{ 'active': selectedNavItem === 'historical-info' }"
        @click="showTSMInfo('historical-info')">歷史資料</button>
      <button class="nav-item" :class="{ 'active': selectedNavItem === 'technical-analysis' }"
        @click="showTSMInfo('technical-analysis')">技術分析</button>
      <button class="nav-item" :class="{ 'active': selectedNavItem === 'financial-analysis' }"
        @click="showTSMInfo('financial-analysis')">財務分析</button>
      <button class="nav-item" :class="{ 'active': selectedNavItem === 'trend-prediction' }"
        @click="showTSMInfo('trend-prediction')">AI預測走勢</button>
    </div>


    <div class="company-details">
      <div v-if="selectedNavItem === 'basic-info'">
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
          <router-view />
        </div>

        <div v-else>
          <p>未找到公司信息</p>
        </div>
      </div>

      <div v-else-if="selectedNavItem === 'historical-info'">
        <h2>歷史資料</h2>
      <p>這裡顯示個股的歷史交易數據或其他相關資訊。</p>
      </div>

      <div v-else-if="selectedNavItem === 'technical-analysis'">
        <div class="technical-analysis-container">
    <h2>技術分析</h2>
    <p>這裡顯示個股的技術分析或其他相關資訊。</p>

    <div class="content-container">
      <div class="buttons-container">
        <!-- MA 按鈕 -->
        <button @click="toggleContent('showMA')">MA</button>
        <!-- RSI 按鈕 -->
        <button @click="toggleContent('showRSI')">RSI</button>
        <!-- KD 按鈕 -->
        <button @click="toggleContent('showKD')">KD</button>
        <!-- MACD 按鈕 -->
        <button @click="toggleContent('showMACD')">MACD</button>
      </div>

      <div class="display-container">
        <div v-if="showMA" class="content-box">
          <h3>MA (移動平均線)</h3>
          <ul>
            <li>
              移動平均線，英文是Moving Average，簡稱MA。<br>
              均線代表市場在過去一段時間內的平均價格，屬於技術分析中的環節。<br>
              是利用統計學上面移動平均的原理來判斷目前大盤的走勢，如果大盤的均線越來越高，代表市場在過去一段時間的趨勢是向上走，反之亦然。
            </li>
          </ul>
        </div>

        <div v-if="showRSI" class="content-box">
          <h3>RSI (相對強弱指標)</h3>
          <ul>
            <li>
              是一種以股價漲跌為基礎，在一段時間內的收盤價，用於評估價格變動的速度(快慢) 與變化(幅度) 的技術分析工具，<br>
              RSI藉由計算一段期間內股價的漲跌變化，判斷最近的趨勢屬於偏強(偏多) 還是偏弱(偏空)。
            </li>
          </ul>
        </div>

        <div v-if="showKD" class="content-box">
          <h3>KD (隨機指標)</h3>
          <ul>
            <li>
              該指標常被用來判斷股價強弱、以及最新股價的相對高低位置，進而尋找價格轉折點，再來決定進場出場的時機。 <br>
              KD指標是由K值跟D值所組成的兩條線圖，用這兩個值來判斷目前價格相對過去一段期間的高低變化，可呈現當天價格目前處於相對高點或低點位置。
            </li>
          </ul>
        </div>

        <div v-if="showMACD" class="content-box">
          <h3>MACD (異同移動平均線)</h3>
          <ul>
            <li>
              MACD是技術分析中非常流行的指標。<br>
              MACD可用於識別證券整體趨勢的各個方面。<br>
              最值得注意的是這些方面是勢頭，以及趨勢方向和持續時間。MACD如此實用的原因在於，它實際上是兩種不同類型指標的組合。<br>
              首先，MACD使用兩條不同長度的移動平均線(滯後指標)來確定趨勢方向和持續時間。然後MACD獲取這兩個移動平均線(MACD線)和這些移動平均線的EMA(訊號線)之間的值差異，並將兩條線之間的差異繪製為在中心零線上方和下方振蕩的直方圖。<br>直方圖被用作證券動量的良好指示。
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
      </div>

      <div v-else-if="selectedNavItem === 'financial-analysis'">
        <div class="financial-analysis-container">
          <h2>財務分析</h2>
          <p>這裡顯示個股的財務分析或其他相關資訊。</p>

          <div class="content-container">
            <div class="buttons-container">
              <!-- Monthly Revenue Button -->
              <button @click="toggleContent('showMA')">月營收</button>
              <!-- Profitability Button -->
              <button @click="toggleContent('showPB')">獲利能力</button>
              <!-- Management Capability Button -->
              <button @click="toggleContent('showMC')">經營能力</button>
              <!-- Shareholder Rights Button -->
              <button @click="toggleContent('showSR')">股東權利</button>
              <!-- Solvency Button -->
              <button @click="toggleContent('showSol')">償債能力</button>
            </div>

            <div class="display-container">
              <div v-if="showMA" class="content-box">
                <h3>月營收</h3>
                <ul>
                  <li>
                    定義：企業銷售產品或提供勞務而取得的收入。<br>

                    營業收入(簡稱營收)是企業尚未扣除任何成本和費用前的收入， 上市櫃公司每個月都得公佈，是財報中最即時的數據。 營收有淡旺季的特性，尤其是電子業有五窮六絕，因此不建議觀察月增率，
                    觀察重點應該是跟去年同期比較，也就是年增率是否成長。
                  </li>
                </ul>
              </div>

              <div v-if="showPB" class="content-box">
                <h3>獲利能力</h3>
                <ul>
                  <li>
                    公司的獲利能力決定企業能否繼續生存，亦即代表公司能否創造足夠的報酬，以吸引投資人投入資金繼續經營。<br>
                    投資人於進行獲利能力分析時，可觀察公司的資產報酬率、股東權益報酬率、純益率、每股盈餘等數據，該等數字愈高時，代表公司的獲利能力愈好。
                  </li>
                </ul>

              </div>

              <div v-if="showMC" class="content-box">
                <h3>經營能力</h3>
                <ul>
                  <li>
                    公是指公司管理者利用公司的資源即資產而達成營運目標的表現，衡量經營者是否有效運用流動資產的指標有應收帳款週轉率、存貨週轉率兩種，衡量是否有效運用固定資產的指標有固定資產週轉率，另尚有總資產週轉率可供參考。<br>
                    這些比率愈高，就代表公司資產的運用效率愈好。
                  </li>
                </ul>
              </div>

              <div v-if="showSR" class="content-box">
                <h3>股東權益</h3>
                <ul>
                  <li>
                    股東權益報酬率代表該年度股東權益的成長速度，計算方式為：<br>
                    股東權益報酬率（ROE）＝（稅後淨利 － 特別股股利發放數）／平均股東權益（OE）<br>
                    其中股東權益為普通股股東權益總額。由股東權益成長率可以看出公司經營階層的目標是否與股東目標一致，而股東權益報酬率係由企業保留盈餘所獲得，因此亦顯示企業如不仰賴對外舉債也能促使其企業成長的能力。
                  </li>
                </ul>
              </div>

              <div v-if="showSol" class="content-box">
                <h3>償債能力</h3>
                <ul>
                  <li>
                    公司的獲利能力決定企業能否繼續生存，亦即代表公司能否創造足夠的報酬，以吸引投資人投入資金繼續經營。<br>
                    投資人於進行獲利能力分析時，可觀察公司的資產報酬率、股東權益報酬率、純益率、每股盈餘等數據，該等數字愈高時，代表公司的獲利能力愈好。
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="selectedNavItem === 'trend-prediction'">
        <h2>AI預測走勢圖</h2>
      <p>首先，時間序列是按照時間軸排序，呈現歷史數據發展過程的資料結構；而時間序列模型，則是依照上述資料結構分析其規律性以及趨勢，並且透過找到概似的軌跡建立模型，用以預測未來的動向。</p>
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
      stockInfo: null,
      otcInfo: null,
      error: null,
      selectedNavItem: 'sii', // Initialize selected navigation item
      showMA1: false,
      showPB: false,
      showMC: false,
      showSR: false,
      showSol: false,
      showMA: false,
      showRSI: false,
      showKD: false,
      showMACD: false
    };
  },
  methods: {
    fetchData() {
      this.isLoading = true;
      let url = '';
      switch (this.selectedNavItem) {
        case 'sii':
          url = 'http://172.16.66.118:8000/STOCK/data?table_name=sii_stock_info';
          break;
        case 'otc':
          url = 'http://172.16.66.118:8000/STOCK/data?table_name=otc_stock_info';
          break;
        default:
          this.isLoading = false;
          return;
      }

      axios.get(url)
        .then(response => {
          this.stockInfo = response.data; // Assume the response data is in the required format
          this.isLoading = false;
        })
        .catch(error => {
          console.error('Fetch error:', error);
          this.error = "Failed to load data";
          this.isLoading = false;
        });
    },

    showTSMInfo(routeName) {
      this.selectedNavItem = routeName;
      this.fetchData(); // Reload data when navigation item changes
    },

    toggleContent(key) {
      // Reset all properties to false
      this.showMA1 = false;
      this.showPB = false;
      this.showMC = false;
      this.showSR = false;
      this.showSol = false;
      this.showMA = false;
      this.showRSI = false;
      this.showKD = false;
      this.showMACD = false;

      // Toggle the specific property
      this[key] = !this[key];
    }
  },
  mounted() {
    this.fetchData(); // Load data when the component mounts
  }
}
</script>



<style scoped>
.company-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.company-table th,
.company-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
  word-wrap: break-word;
}

.company-table th {
  background-color: #f4f4f4;
}

.sidebar{
  text-align: center;
  padding: auto;  
}

.nav-item {
  display: block;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #bed6f1;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.nav-item.active {
  background-color: #65a7ee;
}

h2 {
  color: #333;
  text-align: center;
}

p {
  font-size: 16px;
  text-align: center;
}

.content-container {
  display: flex;

  gap: 20px;
  width: 100%;
}

.buttons-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  max-width: 200px;
  /* Set maximum width */
}

button {
  width: 100%;
  padding: 15px;
  /* Add padding to the buttons */
  font-size: 16px;
  /* Increase button font size */
  background-color: #6ce0aa;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover.company-details {
  background-color: #11b957;
}

.display-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.content-box {
  padding: 20px;
  /* Add padding to content boxes */
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 100%;
  /* Make content box width full */
}

li {
  text-align: left;
}
</style>
