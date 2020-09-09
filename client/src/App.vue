<template>
  <div id="app">
    <meta name="referrer" content="no-referrer"/>
    <router-view/>
  </div>
</template>
<script>
  export default {
    name: 'App',
    created() {
      document.getElementsByTagName('body')[0].className = 'sky'
    }
  }
</script>
<style lang="scss">
@import './assets/css/styles.scss';

* {
    box-sizing: border-box;
    -moz-box-sizing: border-box;
    -webkit-box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  img {
    vertical-align: middle;
    border-style: none;
  }
  a {
    text-decoration: none;
  }
  body {
    transition-duration: 0.3s;
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
    filter: brightness(0.9);
    -moz-filter: brightness(0.9);
    -webkit-filter: brightness(0.9);
  }
  .loading {
    color: white;
    font-size: 24px;
  }
</style>
