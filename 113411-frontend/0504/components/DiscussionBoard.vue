<template>
    <div class="discussion-board">
      <h1>討論區</h1>
      <form @submit.prevent="submitPost">
        <textarea v-model="newPost.content" placeholder="寫點什麼..."></textarea>
        <button type="submit">發布</button>
      </form>
      <div class="posts">
        <div class="post" v-for="post in posts" :key="post.id">
          <h3>{{ post.author }}</h3>
          <p>{{ post.content }}</p>
        </div>
      </div>
    </div>
  </template>
  
  
  <script>

import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      posts: [],
      newPost: {
        content: ''
      }
    };
  },
  computed: {
    ...mapGetters(['username'])
  },
  mounted() {
    this.fetchPosts();
  },
  methods: {
    fetchPosts() {
      axios.get('/api/posts')
        .then(response => {
          this.posts = response.data;
        })
        .catch(error => console.error('Error fetching posts:', error));
    },
    submitPost() {
      if (this.newPost.content.trim()) {
        const post = {
          author: this.username, // 使用 Vuex 获取的用户名
          content: this.newPost.content
        };
        axios.post('/api/posts', post)
          .then(response => {
            this.posts.push(response.data);
            this.newPost.content = '';
          })
          .catch(error => console.error('Error posting:', error));
      }
    }
  }
}
</script>

  
  <style>
  .discussion-board {
    max-width: 800px;
    margin: auto;
  }
  textarea, input {
    width: 100%;
    margin-bottom: 10px;
  }
  .post {
    background-color: #f9f9f9;
    margin-top: 10px;
    padding: 10px;
  }
  </style>
  