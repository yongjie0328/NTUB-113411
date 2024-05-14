// store/modules/auth.js
const state = {
    user: null,
    token: null
  };
  
  const mutations = {
    SET_USER(state, user) {
      state.user = user;
    },
    SET_TOKEN(state, token) {
      state.token = token;
    },
    LOGOUT(state) {
      state.user = null;
      state.token = null;
    }
  };
  
  const actions = {
    logout({ commit }) {
      commit('LOGOUT');
      // 這裡還可以清除本地存儲中的令牌
      localStorage.removeItem('token');
    }
  };
  
  export default {
    state,
    mutations,
    actions
  };
  