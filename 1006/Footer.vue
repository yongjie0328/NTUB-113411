<template>
    <div class="container">
      <!-- 頁尾 -->
      <footer class="footer">
        <a href="https://mops.twse.com.tw/mops/web/index" target="_blank" rel="noopener noreferrer"   class="footer-link">公開資訊觀測站</a>
        <a href="https://news.cnyes.com/news/cat/headline" target="_blank" rel="noopener noreferrer" class="footer-link">鉅亨網</a>
        <a href="https://tw.stock.yahoo.com/" target="_blank" rel="noopener noreferrer" class="footer-link">Yahoo!股市</a>
        <a href="https://www.twse.com.tw/zh/" target="_blank" rel="noopener noreferrer" class="footer-link">TWSE臺灣證券交易所</a>
        <a href="https://www.tpex.org.tw/web/" target="_blank" rel="noopener noreferrer" class="footer-link">證券櫃檯買賣中心</a>
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'FooterForm'
  }
  </script>
  
  <style>
  .container {
    display: flex;
    flex-direction: column;
    height: 100%;
    
  }
  
  .footer {
  display: flex;
  justify-content: space-evenly;  /* 在项之间均匀分布内容 */
  position: fixed;                /* 固定位置，保持在视口底部 */
  left: 0;                        /* 左對齊到视口 */
  bottom: 0;                      /* 底部对齐到视口 */
  width: 100%;                    /* 宽度占满整个视口宽度 */
  padding: 8px 0;                 /* 垂直内边距 */
  background-color: #bcdaed;      /* 背景色 */
  color: white;                   /* 文本颜色 */
  text-align: center;             /* 文本居中 */
  box-sizing: border-box;         /* 边框和内边距不增加宽度 */
}

.footer-link {
  color: #fff;
  text-decoration: none;
  padding: 5px 5px;
  border-radius: px;
  transition: background-color 0.3s;
}

.footer-link:hover {
  background-color: #e0e0e0;
  border-radius: 5px;
}
  </style>
  