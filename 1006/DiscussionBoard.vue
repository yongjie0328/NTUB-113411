<template>
  <div class="discussion-board">
    <form @submit.prevent="publishArticle" class="post-form">
      <label for="article_title">文章標題</label>
      <input type="text" id="article_title" v-model="articleTitle" required>
      <br>
      <label for="article_content">文章內容</label>
      <textarea id="article_content" v-model="articleContent" required></textarea>
      <button type="submit" class="submit-btn">發布</button>
    </form>

    <div class="articles">
      <h2>所有文章</h2>
      <div v-if="loading">載入中...</div>
      <div v-else-if="articles.length === 0">尚無文章</div>
      <div v-else>
        <div v-for="article in articles" :key="article[0]" class="article">
          <h3>標題:{{ article[1] }}</h3>
          <p>內容:{{ article[2] }}</p> <!-- Display the content at index 2 -->
          <p class="article-meta">由 {{ article[4] }} 發佈於 {{ new Date(article[5]).toLocaleString() }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      articleTitle: '',
      articleContent: '',
      articles: [],  // To store articles fetched from the backend
      loading: false
    };
  },
  created() {
    this.fetchArticles();
  },
  methods: {
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    },
    publishArticle() {
      const account = this.getCookie('account');
      if (!account) {
        alert('無法獲取用戶帳號。請確保您已登入。');
        return;
      }

      if (!this.articleTitle || !this.articleContent) {
        alert('文章標題和內容不能為空。');
        return;
      }

      const data = {
        article_title: this.articleTitle,
        article_content: this.articleContent,
        account: account
      };

      fetch('http://172.16.66.118:8000/ARTICLE/publish', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        credentials: 'include'
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('文章發布失敗。請再試一次。');
        }
        return response.json();
      })
      .then(responseData => {
        if (responseData.success) {
          alert('文章發布成功！');
          this.articleTitle = '';
          this.articleContent = '';
          this.fetchArticles();  // Refresh the list of articles after publishing a new one
        } else {
          alert(responseData.message || '由於未知錯誤，文章未能發布。');
        }
      })
      .catch(error => {
        console.error('文章發布時發生錯誤：', error);
        alert('發布您的文章時出錯。請稍後再試。');
      });
    },
    fetchArticles() {
    this.loading = true;
    fetch('http://192.168.50.174:8000/ARTICLE/data', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('無法獲取文章列表。請再試一次。');
        }
        return response.json();
    })
    .then(responseData => {
        this.articles = responseData.content || [];
        this.loading = false;
    })
    .catch(error => {
        console.error('獲取文章列表時發生錯誤：', error);
        alert('獲取文章列表時出錯。請稍後再試。');
        this.loading = false;
    });
}

  }
};
</script>

<style scoped>
body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  background-color: #f8f8f8;
  font-family: Arial, sans-serif;
}

.discussion-board {
  max-width: 600px;
  width: 100%;
  margin: 30px auto;
  padding: 20px;
  margin-top: 100px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.post-form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

textarea {
  resize: vertical;
}

.submit-btn {
  padding: 10px 20px;
  background-color: #7eb6f3;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #2c82de;
}

.articles {
  margin-top: 30px;
}

.article {
  background-color: #f9f9f9;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 10px;
}

.article h3 {
  margin: 0;
}

.article p {
  margin: 10px 0 0 0;
}

.article-meta {
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}
</style>