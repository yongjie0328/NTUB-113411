<template>
  <div class="discussion-board">
    <h1>討論區</h1>
    <div class="posts">
      <!-- 顯示所有帖子的區域 -->
      <div class="post" v-for="post in posts" :key="post.id">
        <h3>{{ post.author }}</h3>
        <p>{{ post.content }}</p>
      </div>
    </div>

    <!-- 固定在底部的發布表單 -->
    <form @submit.prevent="submitPost" class="post-form">
      <textarea v-model="newPost.content" placeholder="寫點什麼..."></textarea>
      <button type="submit" class="submit-btn">發布</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      posts: [], // 用於顯示的帖子
      newPost: {
        content: '' // 新發送的帖子內容
      }
    };
  },
  mounted() {
    // 組件掛載時，獲取所有貼文
    this.fetchPosts();
  },
  methods: {
    // 從後端獲取帖子列表
    fetchPosts() {
      axios.get('/api/posts') // 從後端獲取貼文
        .then((response) => {
          this.posts = response.data; // 將貼文數據存儲到 posts 陣列
        })
        .catch((error) => {
          console.error('Error fetching posts:', error);
        });
    },
    // 發布新貼文
    submitPost() {
      if (this.newPost.content.trim()) {
        const post = {
          author: '您的用戶名', // 替換成適當的用戶名
          content: this.newPost.content
        };
        axios.post('/api/posts', post)
          .then((response) => {
            // 將新的貼文添加到 posts 列表的最後，保持順序
            this.posts.push(response.data);
            // 清空發布區
            this.newPost.content = '';
          })
          .catch((error) => {
            console.error('Error posting:', error);
          });
      }
    }
  }
}
</script>

<style>
.discussion-board {
  max-width: 800px;
  margin: 30px auto 20px auto; /* 在導覽列和討論區之間留出60px的距離 */
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: relative;
}

.post-form {
  position: sticky;
  bottom: 0;
  background-color: #fff;
  padding: 10px;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
  border-radius: 10px 10px 0 0;
  z-index: 10;
}

textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: vertical;
}

.submit-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #0056b3;
}

.posts {
  margin-bottom: 70px; /* 為固定表單預留空間 */
}

.post {
  background-color: #f9f9f9;
  margin-top: 10px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.post h3 {
  margin: 0;
}

.post p {
  margin-top: 5px;
}
</style>
