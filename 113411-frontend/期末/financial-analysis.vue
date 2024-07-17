<template>
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
        <div v-if="showMA1" class="content-box">
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
</template>

<script>
export default {
  name: 'financial-analysis',
  data() {
    return {
      showMA1: false,
      showPB: false,
      showMC: false, // Corrected typo: showMc to showMC
      showSR: false,
      showSol: false,
    };
  },
  methods: {
    toggleContent(key) {
      // Reset all properties to false
      this.showMA1 = false;
      this.showPB = false;
      this.showMC = false;
      this.showSR = false;
      this.showSol = false;
      // Toggle the specific property
      this[key] = !this[key];
    }
  }
}
</script>

<style scoped>
.financial-analysis-container {
  max-width: 100%;
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
