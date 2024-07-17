<template>
    <div class="forgot-password-container">
      <h1>找回密碼</h1>
      <form @submit.prevent="submitEmail">
        <input type="email" v-model="email" placeholder="請輸入你的電子郵件" required>
        <button type="submit">提交</button>
      </form>
    
      <h1>輸入驗證碼</h1>
      <form @submit.prevent="submittext">
        <input type="text" v-model="email" placeholder="請輸入你的驗證碼" required>
        <button type="submit">提交</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: ''
      };
    },
    methods: {
      submitEmail() {
        // 發送電子郵件的邏輯
        alert(`如果 ${this.email} 在我們的系統中，我們將發送一個重設密碼的鏈接到該郵箱。`);
      }
    }
  }
  </script>
  
  <style>
  /* CSS 样式 */
  </style>
  