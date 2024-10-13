<template>
  <div class="financial-table-container">
    <h2>財務分析</h2>
    <p>這裡顯示個股的財務分析或其他相關資訊。</p>
    <table class="financial-table">
      <thead>
        <tr>
          <th colspan="3">償債能力</th>
          <th colspan="3">經營能力</th>
          <th colspan="3">獲利能力</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <!-- 償債能力 -->
          <td>流動比率</td>
          <td>{{ solvencyData.currentRatio }}</td>
          <td></td>
          <!-- 經營能力 -->
          <td>應收款項週轉率</td>
          <td>{{ managementData.receivablesTurnover }}</td>
          <td></td>
          <!-- 獲利能力 -->
          <td>資產報酬率</td>
          <td>{{ profitabilityData.returnOnAssets }}</td>
          <td></td>
        </tr>
        <tr>
          <!-- 償債能力 -->
          <td>速動比率</td>
          <td>{{ solvencyData.quickRatio }}</td>
          <td></td>
          <!-- 經營能力 -->
          <td>平均收現日數</td>
          <td>{{ managementData.avgCollectionPeriod }}</td>
          <td></td>
          <!-- 獲利能力 -->
          <td>權益報酬率</td>
          <td>{{ profitabilityData.returnOnEquity }}</td>
          <td></td>
        </tr>
        <tr>
          <!-- 償債能力 -->
          <td>利息保障倍數</td>
          <td>{{ solvencyData.interestCoverage }}</td>
          <td></td>
          <!-- 經營能力 -->
          <td>存貨週轉率</td>
          <td>{{ managementData.inventoryTurnover }}</td>
          <td></td>
          <!-- 獲利能力 -->
          <td>稅前純益佔實收資本比率</td>
          <td>{{ profitabilityData.preTaxProfitMargin }}</td>
          <td></td>
        </tr>
        <tr>
          <!-- 經營能力 -->
          <td></td>
          <td></td>
          <td></td>
          <td>平均售貨日數</td>
          <td>{{ managementData.avgDaysSales }}</td>
          <td></td>
          <!-- 獲利能力 -->
          <td>純益率</td>
          <td>{{ profitabilityData.netProfitMargin }}</td>
          <td></td>
        </tr>
        <tr>
          <!-- 經營能力 -->
          <td></td>
          <td></td>
          <td></td>
          <td>不動產、廠房及設備週轉率</td>
          <td>{{ managementData.fixedAssetTurnover }}</td>
          <td></td>
          <!-- 獲利能力 -->
          <td>每股盈餘</td>
          <td>{{ profitabilityData.earningsPerShare }}</td>
          <td></td>
        </tr>
        <tr>
          <!-- 經營能力 -->
          <td></td>
          <td></td>
          <td></td>
          <td>總資產週轉率</td>
          <td>{{ managementData.totalAssetTurnover }}</td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      solvencyData: {
        currentRatio: 1.5,
        quickRatio: 1.2,
        interestCoverage: 5.6,
      },
      managementData: {
        receivablesTurnover: 6.5,
        avgCollectionPeriod: 45,
        inventoryTurnover: 4.8,
        avgDaysSales: 30,
        fixedAssetTurnover: 2.1,
        totalAssetTurnover: 1.3,
      },
      profitabilityData: {
        returnOnAssets: '7.5%',
        returnOnEquity: '15%',
        preTaxProfitMargin: '18%',
        netProfitMargin: '12%',
        earningsPerShare: '5.3',
      }
    };
  }
};
</script>

<style scoped>
/* 淡入效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.financial-table-container {
  display: flex;
  justify-content: center;
  margin: 20px auto;
  animation: fadeIn 1.5s ease-in-out; /* 表格淡入效果 */
}

.financial-table {
  width: 100%;
  max-width: 1200px;
  border-collapse: collapse;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.financial-table th, 
.financial-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
  transition: background-color 0.3s ease, color 0.3s ease; /* 背景色和字體顏色過渡效果 */
}

.financial-table th {
  background-color: #f4f4f4;
  font-weight: bold;
  font-size: 18px;
}

.financial-table td {
  font-size: 16px;
}

/* 滑鼠懸停效果：當滑鼠懸停時變換背景顏色 */
.financial-table td:hover {
  background-color: #e0f7fa;
  color: #00695c;
}

/* 過渡效果：當表格內容發生變化時，文字顏色漸變 */
.financial-table td {
  transition: color 0.3s ease, background-color 0.3s ease;
}
</style>
