<template>
  <div class="login">
    <div class="header">
      <img class="img" src="../assets/logo1.jpg" alt="logo" />
    </div>
    <h2>登入</h2>
    <form @submit.prevent="login" id="loginForm" class="input-container">
      <div class="form-group">
        <label for="loginAccount">帳號</label>
        <input type="text" id="loginAccount" v-model="account" required />
      </div>
      <div class="form-group">
        <label for="loginPassword">密碼</label>
        <input :type="passwordVisible ? 'text' : 'password'" id="loginPassword" v-model="password" required />
        <button type="button" @click="togglePasswordVisibility" class="toggle-password">
          <span v-if="passwordVisible">👀</span>
          <span v-else>🙈</span>
        </button>
      </div>
      <button type="submit" class="button">登入</button>
    </form>
    <router-link to="/register" class="btn">註冊</router-link>
    <br />
    <router-link to="/forgot-password" class="forgot-password-link">忘記密碼?</router-link>
    <!-- 错误消息 -->
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'UserLogin',
  data() {
    return {
      account: '',
      password: '',
      passwordVisible: false,
      errorMessage: '', // 用于显示错误消息
    };
  },
  methods: {
    ...mapActions({
      loginUser: 'login', // 映射 Vuex Store 的 login action 为 loginUser
    }),
    async login() {
      try {
        console.log('Trying to login with:', this.account, this.password); // 调试输出
        // 调用 Vuex Store 中的 login 方法
        await this.loginUser({ username: this.account, password: this.password });
        console.log('Login successful'); // 调试输出
        alert('登入成功！');
        this.$router.push('/home'); // 跳转到主页
      } catch (error) {
        // 处理登录失败的情况
        this.errorMessage = '登入失败，请检查您的用户名和密码。';
        console.error('Login failed:', error);
      }
    },
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
    resetForm() {
      this.account = '';
      this.password = '';
      this.errorMessage = ''; // 清空错误消息
    },
  },
};
</script>

<style scoped>
.error {
  color: red;
}
</style>




<style scoped>
/* 設置整個頁面背景，並使內容居中 */
body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  background-color: #D9D4CF; /* 背景色 */
}

/* 登入框樣式 */
.login {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #7C7877; /* 使用指定顏色 */
  border-radius: 5px;
  background-color: #f0e8df;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加陰影效果 */
  background-color: #D9D4CF; /* 背景色 */
}

/* 標題部分樣式 */
.header-login {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

/* 圖片樣式 */
.img {
  width: 110px;
  height: 100px;
}

/* 標題文字顏色 */
.text {
  color: #77AAAD; /* 使用指定顏色 */
  margin: 0;
  font-size: 18px;
}

/* 輸入框容器 */
.input-container {
  text-align: center;
}

/* 表單組 */
.form-group {
  margin-bottom: 15px;
}

/* 標籤樣式 */
label {
  display: block;
  margin-bottom: 5px;
}

/* 輸入框樣式 */
input[type="text"],
input[type="password"] {
  width: 60%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #7C7877; /* 使用指定顏色 */
  border-radius: 5px;
}

/* 按鈕樣式 */
.button {
  background-color: #77AAAD; /* 使用指定顏色 */
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 5px 5px;
  cursor: pointer;
  border-radius: 5px;
}

/* 按鈕懸停效果 */
.button:hover {
  background-color: #7C7877; /* 使用指定顏色 */
}

/* 額外按鈕樣式 */
.btn {
  background-color: #77AAAD; /* 使用指定顏色 */
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 5px 5px;
  cursor: pointer;
  border-radius: 5px;
}

.btn:hover {
  background-color: #7C7877; /* 滑過按鈕時改變顏色 */
}

/* 忘記密碼連結 */
.forgot-password-link {
  display: block;
  margin-top: 10px;
  color: #7C7877; /* 使用指定顏色 */
}

/* 表單組 */
.form-group {
  position: relative;
  margin-bottom: 15px;
}

/* 切換密碼顯示的按鈕 */
.toggle-password {
  background: none;
  border: none;
  cursor: pointer;
  outline: none;
  padding: 5px;
  position: absolute;
  right: 75px;
  top: 68%;
  transform: translateY(-50%);
}
</style>
