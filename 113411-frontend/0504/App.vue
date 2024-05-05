<template>
   <div id="app">
    <Navbar v-if="!$route.meta.hideNavbar" />
    <router-view/>
    <Footer v-if="!$route.meta.hideFooter" />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';

export default {
  components: {
    Navbar,
    Footer
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  align-items: center;

  
}
main {
  flex: 1; /* 强制main区域填充可用空间 */
}

</style>