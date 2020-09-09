<template>
  <div id="nav">
    <nav class="navbar">
      <router-link to="/home" class="navbar-brand">
        <img src="@/assets/images/1.png">
      </router-link>
      <style-button v-for="style in styles" :key="style"
        :colorStyle="style">
      </style-button>
      <template v-if="this.$route.name=='List'">
        <search-input class="nav-input"></search-input>
      </template>
    </nav>
  </div>
</template>

<script>
  import styleButton from '@/components/styleButton'
  import SearchInput from '@/components/SearchInput'
  export default {
    name: 'NavBar',
    data() {
      return {
        showUserInfo: false,
        styles: [
          'sky',
          'nature',
          'planet',
          'twilight'
        ]     
      }
    },
    components: {
      styleButton,
      SearchInput
    }
  }
</script>

<style lang="scss">
  #nav {
    .navbar {
      height: 90px;
      position: sticky;
      position: -webkit-sticky;
      display: flex;
      padding: .5rem 1rem;
      align-items: center;
      .nav-input {
        height: 10px;
        align-items: flex-start;
        margin-left: 20px;
        margin-top: -40px;
        align-self: center;
        input {
          width: 45%;
          &:placeholder {
            font-size: 20px;
          }
        }
      }
    }
    .navbar-brand {
      display: inline-block;
      padding-top: .3125rem;
      padding-bottom: .3125rem;
      margin-right: 1rem;
      font-size: 1.25rem;
      line-height: inherit;
      white-space: nowrap;
    }
    img {
      width: 60px;
      height: 60px;
    }
  }
</style>