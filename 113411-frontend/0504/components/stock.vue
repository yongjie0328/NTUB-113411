<template>
  <div class="stock-layout">
    <nav class="sidebar">
      <router-link to="/stock/basic-info" class="nav-item" :class="{ 'active': isActive('basic-info') }" @click="showTSMInfo('basic-info')">基本資料</router-link>
      <router-link to="/stock/historical-info" class="nav-item" :class="{ 'active': isActive('historical-info') }" @click="showTSMInfo('historical-info')">歷史資料</router-link>
      <router-link to="/stock/technical-analysis" class="nav-item" :class="{ 'active': isActive('technical-analysis') }" @click="showTSMInfo('technical-analysis')">技術分析</router-link>
      <router-link to="/stock/financial-analysis" class="nav-item" :class="{ 'active': isActive('financial-analysis') }" @click="showTSMInfo('financial-analysis')">財務分析</router-link>
      <router-link to="/stock/trend-prediction" class="nav-item" :class="{ 'active': isActive('trend-prediction') }" @click="showTSMInfo('trend-prediction')">AI預測走勢</router-link>
    </nav>
    <div class="main-content">
     
    <router-view/>
  </div>
  </div>
</template>

<script>


export default {
  name: 'StockForm',
  data() {
    return {
      showTSM: true,
      selectedNavItem: null, // 添加一个变量来保存当前选中的导航项
      isLoading: false,
      stockInfo: null // 初始化 stockInfo 为 null
    };
  },
  methods: {
    isActive(routeName) {
      return this.selectedNavItem === routeName; // 修改为检查当前选中的导航项
    },
    showTSMInfo(routeName) {
      if (routeName === 'basic-info') {
        this.showTSM = true;
      } else {
        this.showTSM = false;
      }
      this.selectedNavItem = routeName; // 更新選中的导航项
    }
  }}
   

</script>

<style scoped>
/* 在这里添加样式，根据 selectedNavItem 的值来设置按钮的样式 */


.nav-item.active {
  background-color: #65a7ee;
  transform: scale(1.05);
}

.nav-item {
  margin-right: 10px;
  padding: 8px 12px;
  border: none;
  background-color: #bed6f1;
  color: #fff;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  text-decoration: none;
}
</style>
