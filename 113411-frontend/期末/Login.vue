<template>
  <div class="login">
    <div class="header">
      <img class="img" src="../assets/圖片1.jpg" alt="logo" />
    </div>
    <h2>登入</h2>
    <form @submit.prevent="login" id="loginForm" class="input-container">
      <div class="form-group">
        <label for="loginAccount">帳號</label>
        <input type="text" id="loginAccount" v-model="account" required>
      </div>
      <div class="form-group">
        <label for="loginPassword">密碼</label>
        <input :type="passwordVisible ? 'text' : 'password'" id="loginPassword" v-model="password" required>
        <button type="button" @click="togglePasswordVisibility" class="toggle-password">
          <span v-if="passwordVisible">👀</span>
          <span v-else>🙈</span>
        </button>
      </div>
      <button type="submit" class="button">登入</button>
    </form>
    <router-link to="/register" class="btn">註冊</router-link>
    <br>
    <router-link to="/forgot-password" class="forgot-password-link">忘記密碼?</router-link>
  </div>
</template>

LOGIN
<script>
export default {
  name: 'UserLogin',
  data() {
    return {
      account: '',
      password: '',
      passwordVisible: false
    };
  },
  methods: {
    login() {
      const data = {
        account: this.account,
        password: this.password
      };
      // Execute login operation
      fetch('http://26.134.149.108:8000/USER/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('驗證請求失敗');
        }
        return response.json();
      })
      .then(data => {
        if (data.message === "登入成功") {
          alert('登入成功！');
          // Set a cookie with account information or session data
          document.cookie = `account=${this.account}; path=/; secure; samesite=strict`;
          this.$router.push('/home');  // Use Vue Router to navigate to the home page
        } else {
          alert('帳號或密碼錯誤，請重新輸入');
          this.resetForm();  // Call resetForm method
        }
      })
      .catch(error => {
        console.error('Error during login:', error);
      });
    },
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
    resetForm() {
      this.account = '';
      this.password = '';
    }
  }
};
</script>

<style scoped>
body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}

.login {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.img {
  width: 70px;
  height: 65px;
}

.text {
  color: #86ad7d;
  margin: 0;
  font-size: 18px;
}

.input-container {
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="password"] {
  width: 60%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.button:hover {
  background-color: #1d63af;
}

.btn {
  background-color: #42b983;
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

.forgot-password-link {
  display: block;
  margin-top: 10px;
}

.form-group {
  position: relative;
  margin-bottom: 15px;
}

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
