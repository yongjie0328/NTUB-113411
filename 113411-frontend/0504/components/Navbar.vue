<template>
  <div class="container">
    <!-- 導航列 -->
    <nav class="navbar">
      <div class="nav-left">
        <router-link to="/Home" class="nav-link" :class="{ 'active-link': isActive('/Home') }">首頁</router-link>
        <router-link to="/stock" class="nav-link" :class="{ 'active-link': isActive('/stock') }">個股資訊</router-link>
        <router-link to="/teaching" class="nav-link" :class="{ 'active-link': isActive('/teaching') }">教學小學堂</router-link>
        <router-link to="/risk" class="nav-link" :class="{ 'active-link': isActive('/risk') }">投資評估</router-link>
        <router-link to="/news" class="nav-link" :class="{ 'active-link': isActive('/news') }">新聞</router-link>
        <router-link to="/discussion" class="nav-link" :class="{ 'active-link': isActive('/discussion') }">討論區</router-link>
      </div>
      <div class="nav-right">
        <input type="text" placeholder="搜尋..." class="search-input">
        <router-link to="/profile" class="nav-link" :class="{ 'active-link': isActive('/profile') }">個人資訊</router-link>
        <router-link to="/logout" class="nav-link" :class="{ 'active-link': isActive('/logout') }">登出</router-link>
      </div>
    </nav>
  </div>
</template>

  
<script>
export default {
  name: 'NavbarForm',
  methods: {
    isActive(path) {
      // 这里使用了简单的路径开始匹配，根据项目实际需要调整
      return this.$route.path.startsWith(path);
    }
  }
}
</script>
  
  <style>
  .container {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  * {
  box-sizing: border-box; /* 包括邊界和內間距在內的寬度 */
}
  
  .navbar {
  display: flex; /* 启用Flexbox */
  justify-content: space-between; /* 分散对齐每个项目：在两端对齐，并在项目之间保持等间距 */
  align-items: center; /* 垂直居中所有项目 */
  position: fixed; /* 固定在顶部 */
  top: 0;
  left: 0;
  right: 0;
  width: 100%; /* 覆盖整个视口宽度 */
  background-color: #fff; /* 设置背景颜色 */
  z-index: 1000; /* 确保导航栏在其他内容上方 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* 可选：添加阴影 */
  padding: 10px 20px; /* 内边距 */
}

  .nav-left, .nav-right {
    display: flex;
    
  }
  
  .nav-right {
  flex-shrink: 0; /* 避免.nav-right收縮 */
  flex-wrap: nowrap;
  justify-content: flex-end; /* 元素對齊到右側 */
}


  .nav-link:hover {
  background-color: #f8f9fa;
}
  
  .nav-link {
  white-space: nowrap; 
  margin-right: 10px; /* 減少邊距 */
  padding: 8px 10px; /* 調整填充 */
  color: #333;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}
.active-link {
  background-color: #e0e0e0; /* 淡灰色背景 */
  color: #1a73e8; /* 蓝色文字 */
}

  .nav-link:hover {
  background-color: #e0e0e0; /* Light gray background on hover */
  color: #1a73e8; /* Optional: Change text color on hover */
}

  
  .search-input {
  padding: 8px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s;
  
}

.search-input:hover {
  border-color: #1a73e8; /* Highlight the border of the input box on hover */
}

@media (max-width: 768px) {
  .nav-link, .search-input {
    margin-right: 5px;
    padding: 5px 8px;
  }
}



 
  </style>
  