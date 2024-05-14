<template>
    <div class="dashboard">
      <div class="content-left">
        <h1>台股指數</h1>
        <iframe src="https://s.yimg.com/nb/tw_stock_frontend/scripts/TseChart/TseChart.eb1b267900.html" width="80%" height="500px" frameborder="0"></iframe>
        
      </div>
      <div class="content-right">
        <h2>AI 推薦股票</h2>
        <p>沒東西，隨便放點。</p>
      </div>
    </div>
  </template>
  
  <script>

  
  export default {
    name: 'HomePage',
    components: {
      
    },
    data() {
      return {
        chartData: null
      };
    },
   
  }
  </script>
  
  <style>
  .h1, h2 {
  text-align: center;
}
  .dashboard {
    display: flex;
    padding: 20px;
  }
  
  .content-left {
    flex: 6;
    padding-right: 10px; /* 右侧间隔 */
    justify-content: center;

  }
  
  .content-right {
    flex: 4;
  }
  </style>
  