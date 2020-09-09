<template>
  <div id="search-input">
    <input :placeholder="changePlaceHolder" id="search-bar"
        v-model="keys" @keyup.enter="submitKeys">
    <button class="search-button" 
      @click="changePrefix('Movies')">Movies</button>
    <button class="search-button" 
      @click="changePrefix('Stars')">Stars</button>
    <button class="search-button"
      @click="changePrefix('Comments')">Comments</button>
    <button class="search-button" id="side-button" 
      @click="submitKeys">Search</button>
  </div>
</template>

<script>
  export default {
    name: 'SearchInput',
    data() {
      return {
        prefix: 'Movies',
        keys: ''
      }
    },
    methods: {
      submitKeys() {
        this.$store.dispatch('search/getTotal', {
          type: this.prefix, 
          keys:  this.keys,
          packSize: 16,
          packIndex: 1
        }).then(() => {
          this.$router.push({
            path: '/home/list',
            query: {
              keys: this.keys,
              type: this.prefix,
              page: 1
            }
          })
        })
      },
      changePrefix(value) {
        this.prefix = value
      }
    },
    computed: {
      changePlaceHolder() {
        return 'Enter Something For ' + this.prefix + '...'
      }
    }
  }
</script>

<style lang="scss">
  #search-input {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    margin-top: 20px;
    width: 100%;
    input {
      width: 100%;
      max-width: 500px;
      font-size: 25px;
      border-radius: 1em 3px 3px 1em;
      border-width: 0;
      color: black;
      height: 2em;
      padding: 0 1em;
      outline: medium;
      overflow: visible;
      &::placeholder {
        font-weight: 600;  
        font-size:100%;
      }
    }
    .search-button {
      padding:8px;  
      color: #fff;  
      text-align: center;  
      vertical-align: middle;  
      border: 1px solid transparent;  
      font-weight: 800;  
      font-size:90%;
      height: 50px;
      transition-duration: 0.3s;
      border-radius: 3px;
      outline: none;
      &:hover {
        cursor: pointer;
        transform: scale(1.1, 1.1);
      }
      &:focus {
        color: yellow;
      }
    }
    #side-button {
      background-color: black;
      border-radius: 3px 2em 2em 3px;
    }
  }
</style>