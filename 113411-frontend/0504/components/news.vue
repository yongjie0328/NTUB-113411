<template>
    <div class="news-and-cloud">
      <div class="news-section">
        <h2>新聞區</h2>
        <div class="news-card">
          <h3>新聞標題1</h3>
          <p>這是一個新聞摘要範例，用於展示摘要內容的顯示方式。</p>
          <span class="positive">情緒分析: 正面</span>
        </div>
        <div class="news-card">
          <h3>新聞標題2</h3>
          <p>這是一個新聞摘要範例，用於展示摘要內容的顯示方式。</p>
          <span class="negative">情緒分析: 負面</span>
        </div>
        <div class="news-card">
          <h3>新聞標題3</h3>
          <p>這是一個新聞摘要範例，用於展示摘要內容的顯示方式。</p>
          <span class="neutral">情緒分析: 中立</span>
        </div>
      </div>
  
      <!-- 右側文字雲區域 -->
      <div class="word-cloud-container">
        <div class="word-cloud">
          <h2>文字雲</h2>
          <div class="cloud-placeholder">
            <p>這裡是文字雲的範例位置。</p>
            <!-- 您可以在此嵌入文字雲組件 -->
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NewsAndCloud',
  }
  </script>
  
  <style>
  .news-and-cloud {
    display: flex;
    justify-content: space-between;
    padding: 20px;
  }
  
  .news-section {
    flex: 3; /* 新聞區域佔3個單位 */
    margin-right: 20px;
  }
  
  .word-cloud-container {
    flex: 1; /* 文字雲部分佔1個單位 */
    display: flex;
    justify-content: center;
    align-items: center; /* 置中對齊 */
  }
  
  .word-cloud {
    width: 300px; /* 方框寬度 */
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 80px;
    text-align: center;
  }
  
  .news-card {
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 15px;
    border-radius: 8px;
  }
  
  .news-card h3 {
    margin: 0;
    font-size: 1.5em;
  }
  
  .news-card span.positive {
    color: green;
  }
  
  .news-card span.negative {
    color: red;
  }
  
  .news-card span.neutral {
    color: blue;
  }
  
  .cloud-placeholder {
    color: gray;
  }
  </style>
  