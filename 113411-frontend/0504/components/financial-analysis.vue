<template>
  <div>
    <h2>財務分析</h2>
    <p>這裡顯示個股的財務分析或其他相關資訊。</p>

    <!-- RSI 按鈕 -->
    <button @click="showMR = !showMR">月營收</button>
    <div v-if="showMR">
      <h3>月營收 (企業因銷售產品或提供勞務而取得的各項收入營業收入是企業尚未扣除任何成本和費用前的收入。)</h3>
      <!-- 在這裡顯示RSI相關資訊 -->
    </div>

    <!-- KD 按鈕 -->
    <button @click="showPB = !showPB">獲利能力</button>
    <div v-if="showPB">
      <h3>獲利能力 (企業資金增值的能力)</h3>
      <!-- 在這裡顯示KD相關資訊 -->
    </div>

    <!-- MACD 按鈕 -->
    <button @click="showDP = !showDP ">股利政策</button>
    <div v-if="showDP ">
      <h3>股利政策 (公司在經營過程中，對於股東分配利潤的決策和執行方式。)</h3>
      <!-- 在這裡顯示MACD相關資訊 -->
    </div>

    <!-- DIF 按鈕 -->
    <button @click="showMC = !showMC">經營能力</button>
    <div v-if="showMC">
      <h3>經營能力 (公司管理者利用公司的資源即資產而達成營運目標的表現。)</h3>
      <!-- 在這裡顯示DIF相關資訊 -->
    </div>
    <button @click="showSR = !showSR">股東權利</button>
    <div v-if="showSR">
      <h3>股東權利 (股東對資產清償所有負債後剩餘價值的所有權。)</h3>
      <!-- 在這裡顯示DIF相關資訊 -->
    </div>
    <button @click="showSol = !showSol">償債能力</button>
    <div v-if="showSol">
      <h3>償債能力 (企業償還到期債務的承受能力或保證程度，包括償還短期債務和長期債務的能力。)</h3>
      <!-- 在這裡顯示DIF相關資訊 -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'financial-analysis',
  data() {
    return {
      showMR: false,
      showPB: false,
      showDP: false,
      showMC: false,
      showKD: false,
      showSR: false,
      showSol: false
    };
  }
}
</script>

<style scoped>
/* 在這裡加入組件的樣式 */
h2 {
  color: #333;
}

p {
  font-size: 16px;
}

h3 {
  margin-top: 20px;
}
</style>

  