<template>
  <div class="pr">
    <h1>個人資訊</h1>
    <form @submit.prevent="updateUserInfo" id="updateForm">
      <div class="form-group">
        <label for="account">帳號</label><br>
        <input type="text" id="account" v-model="userInfo.account" required><br>
      </div>
      <div class="form-group">
        <label for="email">信箱</label><br>
        <input type="email" id="email" v-model="userInfo.email" required><br>
      </div>
      <div class="form-group">
        <label for="password">密碼</label><br>
        <input type="password" id="password" v-model="userInfo.password" required><br>
      </div>
      <div class="form-group">
        <label for="gender">性別</label><br>
        <select id="gender" v-model="userInfo.gender" required>
          <option value="男">男</option>
          <option value="女">女</option>
          <option value="其他">其他</option>
        </select><br>
      </div>
      <button type="submit">更新</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'ProfileForm',
  data() {
    return {
      userInfo: {
        account: '',
        email: '',
        password: '',
        gender: ''
      }
    };
  },
  mounted() {
    this.fetchUserInfo();
  },
  methods: {
    fetchUserInfo() {
      fetch('http://140.131.114.169:8001/USER/data?table_name=user_account', {
  method: 'GET',
  credentials: 'include',  // 確保攜帶 cookie
})
.then(response => {
  if (!response.ok) {
    throw new Error('獲取個人資訊失敗');
  }
  return response.json();
})
.then(data => {
  if (data.content) {
    this.userInfo.account = data.content[0];
    this.userInfo.email = data.content[1];
    this.userInfo.password = data.content[2];
    this.userInfo.gender = data.content[3];
  } else {
    alert('獲取個人資訊失敗');
  }
})
.catch(error => {
  console.error('獲取個人資訊失敗:', error);
  alert('獲取個人資訊失敗');
});
},
  updateUserInfo() {
    const data = {
      account: this.userInfo.account,
      password: this.userInfo.password,
      gender: this.userInfo.gender
    };

    // API 根據 cookie 自動識別並更新當前登入使用者的資訊
    fetch('http://140.131.114.169:8001/USER/update-info', {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      credentials: 'include' // 這樣請求會帶上 cookie
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('更新個人資訊失敗，請稍後重試');
      }
      return response.json();
    })
    .then(() => {alert('更新成功！');
    })
    .catch(error => {
      console.error('更新個人資訊失敗:', error);
      alert('更新個人資訊失敗: ' + error.message);
    });
  }
}
}
</script>

<style>
.pr {
  margin-top: 80px;
  text-align: center; /* 將內容置中 */
}

.form-group {
  margin-bottom: 15px;
  display: flex;
  justify-content: center; /* 使表單元素置中 */
  flex-direction: column;
  align-items: center; /* 元素置中 */
}

label {
  margin-bottom: 5px;
  font-size: 18px;
  color: #333;
  text-align: center; /* 標籤文字置中 */
}

input[type="text"],
input[type="email"],
input[type="password"],
select {
  width: 30%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  margin-bottom: 10px; /* 增加下方間距 */
}

button {
  padding: 12px 24px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>
