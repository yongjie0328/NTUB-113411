<template>
    <div class="chart-container">
      <canvas ref="myChart"></canvas>
    </div>
  </template>
  
  <script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    this.createChart();
  },
  methods: {
    createChart() {
      const ctx = this.$refs.myChart.getContext('2d'); // 使用 ref 引用
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
          datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
            
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              
            ],
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  }
}
</script>

  
  <style scoped>
  .chart-container {
    width: 100%;
    height: 500px; /* 或根据需要调整高度 */
  }
  </style>
  