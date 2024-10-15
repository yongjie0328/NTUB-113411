<template>
  <div class="chat-form">
    <div class="logo-container" @click="toggleChat">
      <img src="../assets/圖片1.jpg" alt="Logo" class="logo" />
    </div>
    <div class="chat-window" v-if="isChatOpen" @click.stop>
      <h2>問答機器人</h2>
      <div class="chat-box">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
          <p>{{ message.content }}</p>
        </div>
      </div>
      <div class="input-container">
        <input v-model="userInput" class="input-box" placeholder="問我任何問題..." @keyup.enter="sendMessage" />
        <button @click="sendMessage" class="send-button">發送</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'ChatForm',
  data() {
    return {
      userInput: '',
      messages: [],
      isChatOpen: false,
    };
  },
  methods: {
    toggleChat() {
      this.isChatOpen = !this.isChatOpen; // 切换聊天窗口的开关状态
    },
  async sendMessage() {
    if (!this.userInput) return;
    this.messages.push({ role: 'user', content: this.userInput });

    try {
      // 使用 POST 方法來發送請求
      const response = await axios.post('http://140.131.114.169:8081/ASK/question', {
        question: this.userInput,
      });
      this.messages.push({ role: 'assistant', content: response.data.answer });
    } catch (error) {
      console.error('Error fetching response:', error);
      this.messages.push({ role: 'assistant', content: '無法取得回答，請稍後再試。' });
    }
    this.userInput = '';
  }
  },
};
</script>

<style scoped>
.chat-form {
  position: fixed;
  bottom: 20px;
  right: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logo-container {
  width: 60px;  /* 圆形大小 */
  height: 60px; /* 圆形大小 */
  border-radius: 50%; /* 圆形效果 */
  background-color: #57614e; /* 背景色 */
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3); /* 阴影效果 */
}

.logo {
  width: 50px; /* 根据需要调整 */
  height: 50px; /* 根据需要调整 */
  border-radius: 50%; /* 保持 logo 圆形 */
}

.chat-window {
  width: 400px; /* 聊天窗口宽度 */
  height: 500px; /* 聊天窗口高度 */
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  position: absolute; /* 绝对定位 */
  bottom: 70px; /* 聊天窗口与圆形 logo 的距离 */
  right: 0;
  padding: 20px; /* 增大内边距 */
  z-index: 1000; /* 确保聊天窗口在最上面 */
  display: flex;
  flex-direction: column; /* 让内容垂直排列 */
  font-size: 20px;
}

.chat-box {
  flex-grow: 1; /* 让聊天框填充剩余空间 */
  max-height: 350px; /* 聊天框的最大高度 */
  overflow-y: auto; /* 添加滚动条 */
  margin-bottom: 10px;
  display: flex; /* 使用 Flexbox 进行布局 */
  flex-direction: column; /* 垂直排列 */
}

.message {
  margin:2px 2px;
  padding: 5px;
  border-radius: 5px;
}

.message.user {
  background-color: #e6efeb; /* 用户消息背景色 */
  align-self: flex-end; /* 用户消息右侧对齐 */

}

.message.assistant {
  background-color: #ffffff; /* 助手消息背景色 */
  align-self: flex-start; /* 助手消息左侧对齐 */
}

.input-container {
  display: flex; /* 使用 Flexbox 布局 */
  margin-top: 10px; /* 给输入框和按钮留出空间 */
}

.input-box {
  flex-grow: 1; /* 输入框占据剩余空间 */
  padding: 15px; /* 增大输入框内边距 */
  font-size: 18px; /* 增大字体 */
  border: 1px solid #ccc;
  border-radius: 5px;
}

.send-button {
  padding: 15px; /* 增大按钮的内边距 */
  background-color: #57614e; /* 按钮背景色 */
  color: white; /* 按钮字体颜色 */
  border: none;
  border-radius: 5px;
  font-size: 18px; /* 增大按钮字体 */
  cursor: pointer;
  margin-left: 10px; /* 给按钮留出空间 */
}

.send-button:hover {
  background-color: #47573a; /* 悬停时改变按钮背景色 */
}
</style>
