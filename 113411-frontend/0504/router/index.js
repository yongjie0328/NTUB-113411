import { createRouter, createWebHistory } from 'vue-router';

import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import ForgotPassword from '../components/ForgotPassword.vue';
import Home from '../components/Home.vue';
import Footer from '../components/Footer.vue';
import Navbar from '../components/Navbar.vue';
import DiscussionBoard from '../components/DiscussionBoard.vue';
import store from '../store'; 
import newsForm from '../components/news.vue';

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
    path: '/discussion',
    name: 'discussion',
    component: DiscussionBoard,

  },
  {
    path: '/news',
    name: 'News',
    component: newsForm,

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
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.state.user) {
    next({ name: 'login' });
  } else {
    next();
  }
});



export default router;
