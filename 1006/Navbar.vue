<template>
  <div class="container">
    <!-- 導航列 -->
    <nav class="navbar">
      <div class="nav-left">
        <router-link to="/home" class="nav-link-home-link" :class="{ 'active-link': isActive('/home') }">
          <img class="img" src="../assets/圖片1.jpg" alt="logo" />
        </router-link>
        <router-link to="/stock" class="nav-link" :class="{ 'active-link': isActive('/stock') }">個股資訊</router-link>
        <router-link to="/teaching" class="nav-link" :class="{ 'active-link': isActive('/teaching') }">教學小學堂</router-link>
        <router-link to="/risk" class="nav-link" :class="{ 'active-link': isActive('/risk') }">預測股價</router-link>
        <router-link to="/news" class="nav-link" :class="{ 'active-link': isActive('/news') }">新聞</router-link>
        <!-- <router-link to="/discussion" class="nav-link" :class="{ 'active-link': isActive('/discussion') }">討論區</router-link>-->
        <router-link to="/PortfolioCalculator" class="nav-link" :class="{ 'active-link': isActive('/PortfolioCalculator') }">投資組合計算器</router-link>
      </div>
      <div class="nav-right">
        
        <div class="dropdown" @click="toggleDropdown">
          <span class="nav-link">收藏股票</span>
          <span :class="{'dropdown-arrow': true, 'open': dropdownOpen}"></span>
          <div class="dropdown-content" v-if="dropdownOpen">
            <router-link v-for="stock in favoriteStocks" :key="stock.id" :to="`/stock/${stock.id}`" class="dropdown-item">
              {{ stock.name }}
            </router-link>
          </div>
        </div>
        <router-link to="/profile" class="nav-link" :class="{ 'active-link': isActive('/profile') }">個人資訊</router-link>
        <router-link to="/logout" class="nav-link" :class="{ 'active-link': isActive('/logout') }">登出</router-link>
      </div>
    </nav>

    <!-- 搜尋結果 -->
    <div class="search-results" v-if="searchResults.length">
      <ul>
        <li v-for="result in searchResults" :key="result">{{ result }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavbarForm',
  data() {
    return {
      dropdownOpen: false,
      searchQuery: '',
      searchResults: [],
      favoriteStocks: [
        { id: '2330', name: '2330台積電' },
        { id: '2882', name: '2882國泰金' },
        { id: '2618', name: '2618長榮海運' },
        // 添加更多股票
      ]
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    isActive(route) {
      return this.$route.path === route;
    },
    searchContent() {
      if (this.searchQuery.trim() === '') {
        this.searchResults = [];
        return;
      }

      const query = this.searchQuery.toLowerCase();
      // 模拟搜索内容，这里可以根据实际需要调整逻辑
      const content = [
        '個股資訊',
        '教學小學堂',
        '風險評估',
        '新聞',
        '討論區',
        '個人資訊',
        '登出'
      ];

      this.searchResults = content.filter(item => item.toLowerCase().includes(query));
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
  height: 60px;
  background-color: #fff; /* 设置背景颜色 */
  z-index: 1000; /* 确保导航栏在其他内容上方 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* 可选：添加阴影 */
  padding: 10px 10px; /* 内边距 */
  font-size: 20px;
}

.nav-left, .nav-right {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
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

.nav-link-home-link{
  margin-right: 10px; /* 減少邊距 */
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
  .navbar {
    /* 在小屏幕上将导航栏改为垂直方向 */
    align-items: stretch; /* 拉伸导航栏项目以填充整个宽度 */
  }

  .nav-left, .nav-right {
    /* 在小屏幕上将左右内容改为垂直方向 */
    align-items: center; /* 水平居中 */
  }

  .nav-link, .search-input {
    margin-right: 0; /* 在小屏幕上移除右边距 */
    margin-bottom: 10px; /* 在小屏幕上增加底边距 */
    font-size: 14px; 
  }
}
.dropdown {
  position: relative;
  display: flex;
  align-items: center;
}

.dropdown-content {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
  border-radius: 5px;
  padding: 10px;
}

.dropdown-content .dropdown-item {
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  color: #333;
  cursor: pointer;
}

.dropdown-content .dropdown-item:hover {
  background-color: #f1f1f1;
}

.dropdown-arrow {
  display: inline-block;
  margin-left: 5px; /* 调整箭头与文字之间的距离 */
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid #333;
  transition: transform 0.3s;
}

.dropdown-arrow.open {
  transform: rotate(180deg);
}

.dropdown:hover .dropdown-content {
  display: block;
}

nav img {
  height: 40px; /* 調整logo的高度 */
}
nav .menu-item {
  padding: 10px 20px; /* 調整按鈕的內邊距 */
}

.search-results {
  margin-top: 10px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border-radius: 5px;
  max-height: 200px; /* 限制搜索结果的最大高度 */
  overflow-y: auto; /* 如果结果过多，启用滚动 */
}

.search-results ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.search-results li {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.search-results li:hover {
  background-color: #f8f9fa;
}
</style>
