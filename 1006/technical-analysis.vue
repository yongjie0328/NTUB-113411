<template>
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
</template>

<script>
export default {
  name: 'TechnicalAnalysis',
  data() {
    return {
      showMA: false,
      showRSI: false,
      showKD: false,
      showMACD: false
    };
  },
  methods: {
    toggleContent(key) {
      this.showMA = false;
      this.showRSI = false;
      this.showKD = false;
      this.showMACD = false;
      this[key] = !this[key];
    }
  }
}
</script>

<style scoped>
.technical-analysis-container {
  max-width: 200%;
  margin: auto;
  padding: 20px;
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
  align-items: flex-start;
  gap: 20px;
  width: 100%;
}

.buttons-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  max-width: 200px; /* 固定最大寬度 */
}

button {
  width: 100%;
  padding: 15px; /* 增加按鈕的內邊距 */
  font-size: 16px; /* 增加按鈕的字體大小 */
  background-color: #6ce0aa;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #11b957;
}

.display-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.content-box {
  padding: 20px; /* 增加內容框的內邊距 */
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 100%; /* 讓內容框寬度撐滿 */
}

li {
  text-align: left;
}
</style>
