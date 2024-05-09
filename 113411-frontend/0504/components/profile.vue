<template>
    <div class="profile-form">
      <h2>個人資訊</h2>
      <form @submit.prevent="updateProfile">
        <div class="form-group">
          <label for="username">帳號</label>
          <input type="text" id="username" v-model="user.username" required>
        </div>
        <div class="form-group">
          <label for="email">信箱</label>
          <input type="email" id="email" v-model="user.email" required>
        </div>
        <div class="form-group">
          <label for="gender">性別</label>
          <select id="gender" v-model="user.gender">
            <option value="male">男</option>
            <option value="female">女</option>
            <option value="other">其他</option>
          </select>
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
        user: {
          username: '',
          email: '',
          name: '',
          gender: '', // 預設為男性
        }
      };
    },
    mounted() {
      // 模擬從後端獲取用戶信息
      this.fetchProfile();
    },
    methods: {
      fetchProfile() {
        // 模擬從 API 獲取數據
        const mockProfile = {
          username: 'john_doe',
          email: 'john@example.com',
          gender: 'male',
        };
        this.user = { ...mockProfile };
      },
      updateProfile() {
        // 模擬將更新的個人資料提交到後端
        console.log('更新的個人資訊:', this.user);
        // 這裡可以添加實際的 API 請求邏輯
      }
    }
  }
  </script>
  
  <style scoped>
  .profile-form {
  max-width: 500px;
  margin: 60px auto 20px auto; /* 上方80px，下方20px，左右居中 */
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
}
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input[type="text"],
  input[type="email"],
  select {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  