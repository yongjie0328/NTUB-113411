<template>
  <div class="login">
    <h2>登入</h2>
    <form @submit.prevent="login" class="input-container">
      <div class="form-group">
        <label for="username">帳號</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">密碼</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">登入</button>
    </form>
  
    <router-link to="/Register" class="btn">註冊</router-link>
    <br>
    <router-link to="/forgot-password">忘記密碼?</router-link>
  
  </div>
 <!-- 新增一個 router-link 跳轉到註冊頁面 -->
    

</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      email: '',
      password: ''
    };
  },
  methods: {
    login() {
      console.log('Username:', this.username);
      console.log('Password:', this.password);
      this.$router.push('/home');
    }
  }
};
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
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

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
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
</style>
