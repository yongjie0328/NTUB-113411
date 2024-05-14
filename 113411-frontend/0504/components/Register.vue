<template>
  <div class="register">
    <h2>註冊</h2>
    <form @submit.prevent="register" class="input-container">
      <div class="form-group">
        <label for="username">帳號</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="email">信箱</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="password">密碼</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <div class="form-group">
        <label>性別</label>
        <div class="gender-options">
          <label>
            <input type="radio" value="male" v-model="gender" required> 男
          </label>
          <label>
            <input type="radio" value="female" v-model="gender" required> 女
          </label>
          <label>
            <input type="radio" value="other" v-model="gender" required> 其他
          </label>
        </div>
      </div>
      <button type="submit">註冊</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'RegisterForm',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      gender: '' // 新增的性別欄位
    };
  },
  methods: {
    register() {
      console.log('Username:', this.username);
      console.log('Email:', this.email);
      console.log('Password:', this.password);
      console.log('Gender:', this.gender);
      // 此處可以添加註冊相關的邏輯
    }
  }
};
</script>

<style scoped>
.register {
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

.gender-options {
  justify-content: center;
  display: flex; /* 使用flex排列 */
  gap: 20px; /* 增加每個選項之間的距離 */
}

input[type="text"],
input[type="password"],
input[type="email"] {
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
</style>
