<template>
  <div id="star-info-box">
    <h1 class="hint">
      <span id="main-title">{{starInfo.name}}</span>
    </h1>
    <div id="main-info">
      <div id="mainpic">
        <img :src="starInfo.image" :alt="starInfo.name">
      </div>
      <div id="main-text">
        <span v-if="starInfo.gender !== ''"><span class="info-type">性别：</span><span
          class="info">{{starInfo.gender}}</span></span>
        <span v-if="starInfo.birthDeath !== ''"><span class="info-type">生卒年：</span><span
          class="info">{{starInfo.birthDeath}}</span></span>
        <span v-if="starInfo.occupation !== ''"><span class="info-type">职业：</span><span
          class="info">{{starInfo.occupation}}</span></span>
        <span v-if="starInfo.place !== ''"><span class="info-type">出生地：</span><span
          class="info">{{starInfo.place}}</span></span>
      </div> 
      <div id="description-text">
        <h3>演员简介：</h3>
        <template v-if="lenSmall || total">
          <span v-for="line in starInfo.description" :key="line">{{'\u3000\u3000' + line}}</span>
          <a id="read-button" @click="() => {total=!total}" v-if="!lenSmall">{{'Read Less'}}</a>
        </template>
        <template v-else>
          <span v-for="line in cut(starInfo.description)" :key="line">{{'\u3000\u3000' + line}}</span>
          <a id="read-button" @click="() => {total=!total}">{{'Read More'}}</a>
        </template>
      </div>
    </div>
    <h2 class="hint">
      Related Movies
    </h2>
    <div id="movie-info">
      <info-box v-for="movie in starInfo.movie" :key="movie.id"
        :imgUrl="movie.image" :name="movie.name" :type="'Movies'" :id="movie.id"></info-box>
    </div>
    <h2 class="hint">
      Coorperators
    </h2>
    <div id="co-info">
      <info-box v-for="actor in starInfo.cooperator" :key="actor.id"
        :imgUrl="actor.image" :name="actor.name" :type="'Stars'" :id="actor.id">
        ({{actor.number + ' times'}})</info-box>
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
    this.$store.dispatch('search/getStarInfo', {
      id: this.$route.query.id,
      type: this.$route.query.type
    })
  },
  components: {
    InfoBox
  },
  computed:{
    ...mapState('search', [
      'starInfo'
    ]),
    lenSmall() {
      let len = 0
      for (let i = 0; i < this.starInfo.description.length; ++i) {
        len += this.starInfo.description[i].length
      }
      console.log(len)
      return len <= 500
    }
  },
  methods: {
    cut(list) {
      let len = 0
      let k = 0
      let paras = this.starInfo.description
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
  #star-info-box {
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
        box-shadow: 1px 1px 10px black;
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
    #movie-info {
      margin: 4%;
      display: flex;
      flex-wrap: wrap;
    }
    #co-info {
      margin: 4%;
      display: flex;
      flex-wrap: wrap;
    }
  }
</style>