<template>
  <div class="container">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="nav-left">
        <router-link to="/home" class="nav-link-home-link" :class="{ 'active-link': isActive('/home') }">
          <img class="img" src="../assets/圖片1.jpg" alt="logo" />
        </router-link>
        <router-link to="/teaching" class="nav-link" :class="{ 'active-link': isActive('/teaching') }">教學小學堂</router-link>
        <router-link to="/risk" class="nav-link" :class="{ 'active-link': isActive('/risk') }">AI預測股價</router-link>
        <router-link to="/news" class="nav-link" :class="{ 'active-link': isActive('/news') }">新聞</router-link>
        <router-link to="/PortfolioCalculator" class="nav-link" :class="{ 'active-link': isActive('/PortfolioCalculator') }">投資組合計算器</router-link>
        <router-link to="/StockTracker" class="nav-link" :class="{ 'active-link': isActive('/StockTracker') }">股票價格追蹤</router-link>
      </div>
      <div class="nav-right">
        <!-- 收藏股票下拉列表 -->
        <div class="dropdown" @click="toggleDropdown">
          <span class="nav-link">收藏股票</span>
          <span :class="{'dropdown-arrow': true, 'open': dropdownOpen}"></span>
          <div class="dropdown-content" v-if="dropdownOpen">
            <div v-for="stock in favoriteStocks" :key="stock.id" class="dropdown-item">
              <router-link :to="`/stock/${stock.id}`">
                {{ stock.name }}
              </router-link>
              <!-- 新增刪除按鈕 -->
              <button @click="removeFromFavorites(stock.id)" class="delete-button">刪除</button>
            </div>
          </div>
        </div>
        <router-link to="/profile" class="nav-link" :class="{ 'active-link': isActive('/profile') }">個人信息</router-link>
        <router-link to="/logout" class="nav-link" :class="{ 'active-link': isActive('/logout') }">登出</router-link>
      </div>
    </nav>
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
      favoriteStocks: this.getFavoriteStocks(), // 从 localStorage 获取收藏的股票
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
      const content = [
        '教學小學堂',
        'AI預測股價',
        '新聞',
        '投資組合計算器',
        '股票價格追蹤',
        '收藏股票',
        '個人信息',
        '登出'
      ];

      this.searchResults = content.filter(item => item.toLowerCase().includes(query));
    },
    getFavoriteStocks() {
  let storedStocks = JSON.parse(localStorage.getItem('favoriteStocks')) || [];
  return storedStocks.map(stockCode => ({ id: stockCode, name: `${stockCode}` })); // 修正這裡的 `${stockCode}`
},

    navigateToStockDetails(stockCode) {
    const isFavorite = this.checkIfFavorite(stockCode); // 確定是否已收藏
    this.$router.push({
      name: 'CompanyDetails',
      params: { stockCode, isFavorite }
    });
  },
    checkIfFavorite(stockCode) {
      let favorites = JSON.parse(localStorage.getItem('favoriteStocks')) || [];
      return favorites.includes(stockCode); // 檢查是否在收藏中
    },
    removeFromFavorites(stockCode) {
      // 從 localStorage 中移除股票
      let favorites = JSON.parse(localStorage.getItem('favoriteStocks')) || [];
      favorites = favorites.filter(code => code !== stockCode);
      localStorage.setItem('favoriteStocks', JSON.stringify(favorites));
      // 更新列表
      this.favoriteStocks = this.getFavoriteStocks();
    }
  },
  mounted() {
    this.favoriteStocks = this.getFavoriteStocks();
    // 监听网页加载时更新收藏列表
    window.addEventListener('storage', () => {
      this.favoriteStocks = this.getFavoriteStocks();
    });
  },
};
</script>

<style scoped>
.container {
  margin-top: 80px;
  display: flex;
  flex-direction: column;
  height: 100%;
}
* {
  box-sizing: border-box;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: 60px;
  background-color: #fff;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 10px 10px;
  font-size: 20px;
}

.nav-left, .nav-right {
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-right {
  flex-shrink: 0;
  flex-wrap: nowrap;
  justify-content: flex-end;
}

.nav-link:hover {
  background-color: #f8f9fa;
}

.nav-link {
  white-space: nowrap;
  margin-right: 10px;
  padding: 8px 10px;
  color: #333;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.nav-link-home-link{
  margin-right: 10px; /* 減少邊距 */
}

.active-link {
  background-color: #e0e0e0;
  color: #1a73e8;
}

.nav-link:hover {
  background-color: #e0e0e0; 
  color: #1a73e8; 
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
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  border-radius: 5px;
  padding: 10px;
}

.dropdown-content .dropdown-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px;
  color: #333;
  cursor: pointer;
}

.dropdown-content .dropdown-item:hover {
  background-color: #f1f1f1;
}

.dropdown-arrow {
  display: inline-block;
  margin-left: 5px;
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

.delete-button {
  background-color: #ff6666;
  color: white;
  border: none;
  padding: 5px;
  border-radius: 5px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: #ff3333;
}

nav img {
  height: 40px; /* 調整logo的高度 */
}
</style>
