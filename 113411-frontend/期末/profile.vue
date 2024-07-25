<template>
  <div  class="pr">
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
        gender: ''
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
          console.log('Data received:', data);
          if (data.content) {
              this.userInfo.account = data.content[0];
              this.userInfo.email = data.content[1]; 
              this.userInfo.password = data.content[2]; 
              this.userInfo.gender = data.content[3];
          } else {
              console.error('Data content is missing or invalid:', data);
              alert('獲取個人資訊失敗');
          }
      })
      .catch(error => {
          console.error('獲取個人資訊失敗:', error);
          alert('獲取個人資訊失敗');
      });
    },
    updateUserInfo() {
      const form = document.getElementById('updateForm');
      const account = form.account.value;
      const password = form.password.value;
      const gender = form.gender.value;

      const data = {
          account: account,
          password: password,
          gender: gender
      };

      console.log('Sending data:', data); // 調試信息
      fetch('http://172.16.66.118:8000/USER/update-info', {
          method: 'PATCH',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
          credentials: 'include'
      })
      .then(response => {
          console.log('Response:', response);
          if (!response.ok) {
              throw new Error('更新個人資訊失敗，請稍後重試');
          }
          return response.json();
      })
      .then(data => {
          console.log('Received data:', data);
          alert(data.message);
          const updatedInfo = data.updated_info;
          if (updatedInfo.account) {
              this.userInfo.account = updatedInfo.account;
          }
          if (updatedInfo.password) {
              this.userInfo.password = updatedInfo.password;
          }
          if (updatedInfo.gender) {
              this.userInfo.gender = updatedInfo.gender;
          }
          form.reset(); // 重置表單
      })
      .catch(error => {
          console.error('Fetch error:', error);
          alert('更新個人資訊失敗: ' + error.message);
      });
    }
  }
};
</script>

<style>
.pr{
  margin-top: 80px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-size: 18px;
  color: #333;
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
