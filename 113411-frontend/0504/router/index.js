// Import Vue Router 方法
import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import ForgotPassword from '../components/ForgotPassword.vue';
import Home from '../components/Home.vue';
import Footer from '../components/Footer.vue';
import Navbar from '../components/Navbar.vue';
import DiscussionBoard from '../components/DiscussionBoard.vue';
import riskForm from '../components/risk.vue';
import TeachingForm from '../components/teaching.vue';
import store from '../store'; 
import NewsForm from '../components/news.vue';
import StockForm from '../components/stock.vue';
import BasicInfo from '../components/BasicInfo.vue';
import HistoricalInfo from '../components/historical-info.vue';
import TechnicalAnalysis from '../components/technical-analysis.vue';
import ProfileForm from '../components/profile.vue';
import FinancialAnalysis from '../components/financial-analysis.vue';
import TrendPrediction from '../components/trend-prediction.vue';

// 組合所有路由
const routes = [
  {
    path: '/',
    name: 'login',
    component: Login,
    meta: { hideNavbar: true, hideFooter: true }
  },
  {
    path: '/home',
    name: 'home',
    components: {
      default: Home,
      navbar: Navbar,
      footer: Footer
    }
  },
  {
    path: '/logout',
    name: 'logout',
    redirect: { name: 'login' } // 將登出導向到登入頁面
  },
  {
    path: '/discussion',
    name: 'discussion',
    component: DiscussionBoard,
  },
  {
    path: '/news',
    name: 'news',
    component: NewsForm,
  },
  {
    path: '/risk',
    name: 'risk',
    component: riskForm,
  },
  {
    path: '/teaching',
    name: 'teaching',
    component: TeachingForm,
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileForm,
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: { hideNavbar: true, hideFooter: true }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPassword,
    meta: { hideNavbar: true, hideFooter: true }
  },
  {
    path: '/stock',
    component: StockForm,
    children: [
      { path: 'basic-info', component: BasicInfo }, // 移除前导斜杠
      { path: 'historical-info', component: HistoricalInfo },
      { path: 'technical-analysis', component: TechnicalAnalysis },
      { path: 'financial-analysis', component: FinancialAnalysis },
      { path: 'trend-prediction', component: TrendPrediction }
    ]
  }
];

// 創建路由器
const router = createRouter({
  history: createWebHistory(),
  routes
});

// 路由導航守衛
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.state.user) {
    next({ name: 'login' });
  } else {
    next();
  }
});

// 導出路由器
export default router;
