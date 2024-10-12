<template>
  <div class="forgot-password-container">
    <h1>找回密碼</h1>
    <form @submit.prevent="submitEmail">
      <input type="email" v-model="email" placeholder="請輸入你的電子郵件" required>
      <button type="submit">提交</button>
    </form>

    <h1>輸入驗證碼</h1>
    <form @submit.prevent="submitText">
      <input type="text" v-model="verificationCode" placeholder="請輸入你的驗證碼" required>
      <button type="submit">提交</button>
    </form>

    <!-- Return to Login Button -->
    <button @click="returnToLogin" class="return-button">返回登入頁面</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      verificationCode: ''
    };
  },
  methods: {
    submitEmail() {
      // 發送電子郵件的邏輯
      alert(`如果 ${this.email} 在我們的系統中，我們將發送一個重設密碼的鏈接到該郵箱。`);
    },
    submitText() {
      // 提交驗證碼的邏輯
      alert(`你已提交驗證碼: ${this.verificationCode}`);
    },
    returnToLogin() {
      // 返回登入頁面的邏輯，例如使用 Vue Router
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.center-wrapper {
  display: flex;
  justify-content: center; /* 水平置中 */
}

.forgot-password-container {
  max-width: 400px; /* 設置容器的最大寬度 */
  padding: 20px;
  border: 1px solid #7C7877;
  border-radius: 8px;
  background-color: #D9D4CF;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  flex-direction: column; /* 垂直排列內容 */
  align-items: center;
  text-align: center;
}

h1 {
  text-align: center;
  color: #7C7877;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

input[type="email"],
input[type="text"] {
  width: 80%;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 16px;
  border: 1px solid #7C7877;
  border-radius: 5px;
  background-color: #fff;
}

button {
  width: 50%;
  padding: 10px;
  background-color: #7C7877;
  color: #D9D4CF;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
}

button:hover {
  background-color: #605e5d;
}

.return-button {
  background-color: #605e5d; /* Different color for the return button */
}

.return-button:hover {
  background-color: #403f3e;
}
</style>
