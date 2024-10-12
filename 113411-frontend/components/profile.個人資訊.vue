<template>
  <div class="pr">
    <h1>個人資訊</h1>
    <form @submit.prevent="updateUserInfo">
      <div class="form-group">
        <label for="account">帳號</label><br>
        <input type="text" id="account" v-model="userInfo.account"><br>
      </div>
      <div class="form-group">
        <label for="email">信箱</label><br>
        <input type="email" id="email" v-model="userInfo.email"><br>
      </div>
      <div class="form-group">
        <label for="password">密碼</label><br>
        <input type="password" id="password" v-model="userInfo.password"><br>
      </div>
      <div class="form-group">
        <label for="gender">性別</label><br>
        <select id="gender" v-model="userInfo.gender">
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
        gender: '',
        ticker: '',
        targetPrice: '',
        responseMessage: ''
      }
    };
  },
  mounted() {
    this.fetchUserInfo();
  },
  methods: {
    fetchUserInfo() {
      fetch('http://192.168.50.174:8000/USER/data', {
        credentials: 'include'
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

      fetch('http://172.16.66.118:8000/USER/update-info', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        credentials: 'include'
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('更新個人資訊失敗，請稍後重試');
        }
        return response.json();
      })
      .then(data => {
        alert(data.message);
        this.userInfo.account = data.updated_info.account || this.userInfo.account;
        this.userInfo.password = data.updated_info.password || this.userInfo.password;
        this.userInfo.gender = data.updated_info.gender || this.userInfo.gender;
      })
      .catch(error => {
        console.error('Fetch error:', error);
        alert('更新個人資訊失敗: ' + error.message);
      });
    },
   
  }
};
</script>

<style>
.pr{
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