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
        <label for="gender">性別</label>
        <select id="gender" v-model="gender" required>
          <option value="male">男</option>
          <option value="female">女</option>
          <option value="other">其他</option>
        </select>
      </div>
      <button type="submit" class="reg">註冊</button>
    </form>
    <router-link to="/" class="login">返回登入</router-link>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'UserRegister',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      gender: ''
    };
  },
  methods: {
    ...mapActions(['setUser']),
    register() {
      const data = {
        username: this.username,
        email: this.email,
        password: this.password,
        gender: this.gender
      };

      fetch('http://140.131.114.169:8001/USER/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('註冊請求失敗');
        }
        return response.json();
      })
      .then(data => {
        console.log('Success:', data);
        if (data.message === "註冊成功") {
          alert('註冊成功！');
          this.setUser({
            username: this.username,
            email: this.email,
            password: this.password,
            gender: this.gender
          });
          this.$router.push('/profile');
        } else {
          alert('註冊失敗，請重新輸入');
          this.resetForm();
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('註冊失敗，請稍後再試。');
        this.resetForm();
      });
    },
    resetForm() {
      this.username = '';
      this.email = '';
      this.password = '';
      this.gender = '';
    }
  }
};
</script>

<style scoped>
.center-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* 確保內容垂直居中 */
}

.register {
  width: 100%; /* 讓容器在手機等小屏幕上自適應 */
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #7C7877;
  border-radius: 5px;
  background-color: #D9D4CF;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加陰影效果 */
}

.input-container {
  display: flex;
  flex-direction: column; /* 將元素垂直排列 */
  align-items: center; /* 確保輸入框和按鈕水平居中 */
  text-align: center;
}

.form-group {
  width: 100%;
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  display: block;
  margin-bottom: 5px;
  width: 100%; /* 讓標籤與輸入框寬度一致 */
  text-align: center;
}

input[type="text"],
input[type="password"],
input[type="email"],
select {
  width: 80%; /* 增加寬度來自適應屏幕 */
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box; /* 包括 padding 在內的寬度 */
  text-align: center;
}
select {
  width: 60%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
}


button.reg {
  width: 80%;
  background-color: #77AAAD;
  color: #fff;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
}

.login {
  background-color:#403f3e;
  color: #fff;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  text-decoration: none;
  margin-top: 10px;
}

button:hover {
  background-color: #7C7877;
}
</style>
