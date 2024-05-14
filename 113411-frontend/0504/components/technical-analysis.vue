<template>
  <div>
    <h2>技術分析</h2>
    <p>這裡顯示個股的技術分析或其他相關資訊。</p>

    <!-- RSI 按鈕 -->
    <button @click="showRSI = !showRSI">RSI</button>
    <div v-if="showRSI">
      <h3>RSI (相對強弱指標)</h3>
      <!-- 在這裡顯示RSI相關資訊 -->
    </div>

    <!-- KD 按鈕 -->
    <button @click="showKD = !showKD">KD</button>
    <div v-if="showKD">
      <h3>KD (隨機指標)</h3>
      <!-- 在這裡顯示KD相關資訊 -->
    </div>

    <!-- MACD 按鈕 -->
    <button @click="showMACD = !showMACD">ACD</button>
    <div v-if="showMACD">
      <h3>MACD (異同移動平均線)</h3>
      <!-- 在這裡顯示MACD相關資訊 -->
    </div>

    <!-- DIF 按鈕 -->
    <button @click="showDIF = !showDIF">DIF</button>
    <div v-if="showDIF">
      <h3>DIF (差離值)</h3>
      <!-- 在這裡顯示DIF相關資訊 -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'technical-analysis',
  data() {
    return {
      showRSI: false,
      showKD: false,
      showMACD: false,
      showDIF: false
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
