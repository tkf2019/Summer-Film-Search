<template>
  <div id="movie-info-box">
    <h1 class="hint">
      <span id="main-title">{{movieInfo.name}}</span>
      <span id="year" v-if="getYear !== ''">({{getYear}})</span>
    </h1>
    <div id="main-info">
      <div id="mainpic">
        <img :src="movieInfo.image" :alt="movieInfo.name">
      </div>
      <div id="main-text">        
        <span v-if="movieInfo.director.length != 0"><span class="info-type">导演：</span><span class="info">
          {{getList(movieInfo.director)}}</span></span>
        <span v-if="movieInfo.author.length != 0"><span class="info-type">编剧：</span><span class="info">
          {{getList(movieInfo.author)}}</span></span>
        <span v-if="movieInfo.genre.length != 0"><span class="info-type">类型：</span><span class="info">
          {{getList(movieInfo.genre)}} </span></span>
        <span v-if="movieInfo.language !== ''"><span class="info-type">语言：</span><span
          class="info">{{movieInfo.language}}</span></span>
        <span v-if="movieInfo.date !== ''"><span class="info-type">上映时间：</span><span
          class="info">{{movieInfo.date}}</span></span>
        <span v-if="movieInfo.time !== ''"><span class="info-type">片长：</span><span
          class="info">{{movieInfo.time}}</span></span>
        <span v-if="movieInfo.score !== ''"><span class="info-type">豆瓣评分：</span>
          <span class="info">{{movieInfo.score}}分</span></span>
      </div> 
      <div id="description-text">
        <h3>影片简介：</h3>
        <template v-if="lenSmall || total">
          <span v-for="line in movieInfo.description" :key="line">{{'\u3000\u3000' + line}}</span>
          <a id="read-button" @click="() => {total=!total}" v-if="!lenSmall">{{'Read Less'}}</a>
        </template>
        <template v-else>
          <span v-for="line in cut(movieInfo.description)" :key="line">{{'\u3000\u3000' + line}}</span>
          <a id="read-button" @click="() => {total=!total}">{{'Read More'}}</a>
        </template>
      </div>
    </div>
    <h2 class="hint">
      Related Actors
    </h2>
    <div id="actor-info">
      <info-box v-for="star in movieInfo.actor" :key="star.id"
        :imgUrl="star.image" :name="star.name" :type="'Stars'" :id="star.id"></info-box>
    </div>
    <h2 class="hint">
      Comments
    </h2>
    <div id="comment-text">
      <span v-for="line in movieInfo.comment" :key="line"
       class="comment-span">{{'\u3000\u3000' + line}}</span>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import InfoBox from '@/components/infoBox'
export default {
  name: 'Info',
  data() {
    return {
      total: false
    }
  },
  mounted() {
    this.$store.dispatch('search/getMovieInfo', {
      id: this.$route.query.id,
      type: this.$route.query.type
    })
  },
  components: {
    InfoBox
  },
  computed:{
    ...mapState('search', [
      'movieInfo'
    ]),
    getYear() {
      return this.movieInfo.date.split('-')[0]
    },
    lenSmall() {
      let len = 0
      for (let i = 0; i < this.movieInfo.description.length; ++i) {
        len += this.movieInfo.description[i].length
      }
      return len <= 500
    }
  },
  methods: {
    getList(list) {
      let ret = ''
      for(let i = 0; i < list.length - 1; ++i) {
        ret += list[i] + ' / '
      }
      return ret + list[list.length - 1]
    },
    cut(list) {
      let len = 0
      let k = 0
      let paras = this.movieInfo.description
      let ret = []
      for (let i = 0; i < paras.length; ++i) {
        len += paras[i].length
        if (len > 500) {
          k = i
          break
        }
        ret.push(paras[i])
      }
      ret.push(paras[k].slice(0, 350) + '......')
      return ret
    }
  }
}
</script>

<style lang="scss">
  #movie-info-box {
    .hint {
      text-align: center;
      font-size: 36px;
      font-weight: bold;
      color: white;
      line-height: 1.1;
      #year {
        color: #888;
      }
    }
    #main-info {
      display: flex;
      height: 30%;
    }
    #mainpic {
      width: 20%;
      margin: 4%;
      margin-left: 2%;
      img {
        border-radius: 10px;
        box-shadow: 1px 4px 10px black;
        width: 100%;
      }
    }
    #main-text {
      width: 20%;
      margin-bottom: 4%;
      margin-top: 6%;
      font-size: 16px;
      font-family: Helvetica,Arial,sans-serif;
      color: white;
      span {
        word-wrap: break-word;
        word-break: normal;
        line-height: 40px;
        display: flex;
      }
      .info-type {
        font-weight: bold;
        display: inline;
        white-space: nowrap;
      }
    }
    #description-text {
      width: 50%;
      height: auto;
      margin: 2%;
      margin-top: 6%;
      font-size: 14px;
      font-family: Helvetica,Arial,sans-serif;
      color: white;
      span {
        word-break: normal;
        line-height: 40px;
        display: flex;
      }
      #read-button {
        font-size: 20px;
        transition-duration: 0.3s;
        text-decoration: underline;
        &:hover {
          cursor: pointer;
          color: yellow;
          transform: scale(1.1, 1.1);
        }
      }
    }
    #actor-info {
      margin: 4%;
      display: flex;
      flex-wrap: wrap;
    }
    #comment-text {
      align-self: center;
      width: 60%;
      height: auto;
      margin-left: 20%;
      margin-top: 6%;
      font-size: 14px;
      font-family: Helvetica,Arial,sans-serif;
      color: white;
      .comment-span {
        border-radius: 10px;
        color: white;
        margin: 20px auto;
        padding: 10px 20px;
        word-break: normal;
        line-height: 40px;
        display: flex;
        box-shadow: 1px 1px 10px black;
      }
    }
  }
</style>