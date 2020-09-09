<template>
  <div class="info-box">
    <img :src="imgUrl" :alt="name" 
      referrer="no-referrer|origin|unsafe-url" @click="jumpToInfo">
    <p class="info-name" @click="jumpToInfo">{{name}}<slot></slot></p>
  </div>
</template>

<script>
export default {
  name: 'InfoBox',
  props: {
    imgUrl: '',
    name: '',
    id: '',
    type: ''
  },
  methods: {
    jumpToInfo() {
      const searchType = this.type
      if (searchType === 'Movies' || searchType === 'Comments') {
        this.$store.dispatch('search/getMovieInfo', {
          id: this.id,
          type: searchType
        }).then(() => {
          this.$router.push({
            path: '/home/movie',
            query: {
              id: this.id,
              type: searchType
            }
          })
        })
      } else if (searchType == 'Stars') {
        console.log('Stars')
        this.$store.dispatch('search/getStarInfo', {
          id: this.id,
          type: searchType
        }).then(() => {
          this.$router.push({
            path: '/home/star',
            query: {
              id: this.id,
              type: searchType
            }
          })
        })
      }
    }
  }
}
</script>

<style lang="scss">
  .info-box {
    margin: auto;
    width: 20%;
    height: 26%;
    max-width: 180px;
    border-radius: 10px;
    transition-duration: 0.3s;
    justify-content: center;
    float: left;
    &:hover {
      transform: translateY(-5px);
    }
    img {
      width: 80%;
      border-radius: 10px;
      margin-left: 10%;
      margin-right: auto;
      margin-top: 5px;
      box-shadow: 1px 1px 10px black;
      &:hover {
        cursor: pointer;
      }
    }
    .info-name {
      width: 100%;
      color: white;
      text-align: center;
      padding: 2px;
      padding-top: 6px;
      font-size: 16px;
      &:hover {
        text-decoration: underline;
        cursor: pointer;
      }
    }
  }
</style>