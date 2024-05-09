<template>
  <div>
    <canvas v-if="isCanvasVisible" ref="myChart"></canvas>
    <!-- 其他 UI 內容 -->
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'DiscussionBoard',
  data() {
    return {
      isCanvasVisible: true,
    };
  },
  mounted() {
    this.initChart();
  },
  methods: {
    initChart() {
      // 確保 `<canvas>` 已經渲染到 DOM 中
      const canvas = this.$refs.myChart;

      if (canvas) {
        const ctx = canvas.getContext('2d');

        // 初始化 Chart.js 圖表
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['January', 'February', 'March'],
            datasets: [
              {
                label: 'Sample Data',
                data: [10, 20, 30],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          },
        });
      } else {
        console.error('Canvas element is not available');
      }
    },
  },
};
</script>

<style scoped>
canvas {
  width: 100%;
  height: 400px;
}
</style>
