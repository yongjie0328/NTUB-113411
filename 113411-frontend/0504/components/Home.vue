<template>
    <div class="dashboard">
      <div class="content-left">
        <h1>台股指數</h1>
        <p>還沒東西，隨便放點。</p>
        <ChartComponent :chartData="chartData" />
      </div>
      <div class="content-right">
        <h2>AI 自動推薦股票</h2>
        <p>沒東西，隨便放點。</p>
      </div>
    </div>
  </template>
  
  <script>
  import ChartComponent from './ChartComponent.vue';
  import axios from 'axios';
  
  export default {
    name: 'HomePage',
    components: {
      ChartComponent
    },
    data() {
      return {
        chartData: null
      };
    },
    mounted() {
      this.fetchChartData();
    },
    methods: {
      fetchChartData() {
        // 假设使用 axios 获取数据
        axios.get('/api/chart-data')
          .then(response => {
            this.chartData = response.data;
          })
          .catch(error => console.error('Error fetching chart data:', error));
      }
    }
  }
  </script>
  
  <style>
  .dashboard {
    display: flex;
    padding: 20px;
  }
  
  .content-left {
    flex: 6;
    padding-right: 20px; /* 右侧间隔 */
  }
  
  .content-right {
    flex: 4;
  }
  </style>
  