// store/index.js
import { createStore } from 'vuex';
import axios from 'axios';
import router from '../router'; // 确保路径正确

export default createStore({
  state: {
    user: null
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    }
  },
  actions: {
    login({ commit }, { username, password }) {
      axios.post('/api/login', { username, password })
        .then(response => {
          commit('setUser', response.data.user);
          router.push('/home'); // 使用 router 实例
        })
        .catch(error => {
          console.error('Login failed:', error);
        });
    }
  },
  getters: {
    username: state => state.user ? state.user.username : '',
    isUserLoggedIn: state => !!state.user
  }
});
