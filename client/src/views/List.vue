<script>
  import { mapState } from 'vuex'
  import paging from '@/components/paging'
  import InfoBox from '@/components/infoBox' 
  export default {
    name: 'List',
    data() {
      return {
        page: 1
      }
    },
    mounted() {
      this.$store.dispatch('search/getTotal', {
        keys: this.$route.query.keys,
        type: this.$route.query.type,
        packSize: 16,
        packIndex: this.$route.query.page
      })
    },
    components: {
      paging,
      InfoBox
    },
    render(h) {
      let boxList = []
      let articleBox = []
      const articleNumber = this.searchData.number
      const time = this.searchData.time
      const searchType = this.$route.query.type
      const len = this.searchData.results.length
      if (searchType === 'Movies' || searchType === 'Stars') {
        const boxes = this.searchData.results
        for (let i = 0; i < len; ++i) {
          boxList.push(h(InfoBox, {
            props: {
              imgUrl: boxes[i].image,
              name: boxes[i].name,
              id: boxes[i].id,
              type: this.$route.query.type
            }
          }))
        }
      } else if (searchType == 'Comments') {
        let pageList = []
        const articles = this.searchData.results
        const pageNumber = Math.ceil(articleNumber / 16)
        const maxPagePack = Math.ceil(pageNumber / 5)
        const keys = this.$route.query.keys

        function highlight(string) {
          let resultString = ''
          let lastIndex = 0
          let nowIndex = string.indexOf(keys)
          
          while (true) {
            if (nowIndex != -1) {
              resultString += string.substring(lastIndex, nowIndex)
                + '<span class=\"highlight\">' + keys + '<\/span>'
            } else {
              resultString += string.substring(lastIndex)
              break
            }

            lastIndex = nowIndex + keys.length
            nowIndex = string.indexOf(keys, nowIndex + 1)
          }
          return resultString
        }
        for (let i = 0; i < 16; i++) {
          if (16 * (this.page - 1) + i >= articleNumber) {
            break
          }
          let contentList = []
          let contentPart = ''
          let firstIndex = articles[i].comment.indexOf(keys)          
          let titlePart = highlight(articles[i].name) + '（' + articles[i].score + '分）'

          if (firstIndex < 200) {
            contentPart = highlight(articles[i].comment.substring(0, 200)) + '......'
          } else {
            contentPart = '......' + highlight(articles[i].comment.substring(firstIndex - 100, firstIndex + 100)) + '......'
          }
          contentPart += `(<span class=\"highlight\">${articles[i].times} times</span>)`

          contentList.push(h('div', {
            class: 'left-content'
          }, [
            h('img', {
              domProps: {
                src: articles[i].image
              }
            })
          ]))
          contentList.push(h('div', {
            class: 'right-content'
          }, [
            h('a', {
              class: 'post-title',
              domProps: {
                innerHTML: `${titlePart}`
              },
              on: {
                click: () => {
                  this.$store.dispatch('search/getMovieInfo', {
                    id: articles[i].id,
                    type: 'Movies'
                  }).then(() => {
                    this.$router.push({
                      path: '/home/movie',
                      query: {
                        id: articles[i].id,
                        type: 'Movies'
                      }
                    })
                  })
                }
              }
            }),
            h('p', {
              class: 'post-content',
              domProps: {
                innerHTML: `${contentPart}`
              }
            })
          ]))
          articleBox.push(h('div', {
            class: 'article-content'
          }, contentList))
        }
      }
      
      return h('div', [
        h('p', {
          domProps: {
            innerHTML: `Took <strong>${time == '' ? 0 : time}</strong> to search 
              <strong>${articleNumber}</strong> relevant results.`
          },
          class: 'search-summary'
        }),
        h('div', {
          class: 'list'
        }, boxList),
        h('div', {
          class: 'article-box'
        }, articleBox),
        h(paging, {
          on: {
            changePage: page => {
              this.$store.dispatch('search/getTotal', {
                type: this.$route.query.type, 
                keys:  this.$route.query.keys,
                packSize: 16,
                packIndex: page
              }).then(() => {
                this.$router.push({
                  path: '/home/list',
                  query: {
                    keys: this.$route.query.keys,
                    type: this.$route.query.type,
                    page: page
                  }
                })
              })
            }
          }
        })
      ])
    },
    computed: mapState('search', [
      'searchData'
    ])
  }
</script>

<style lang="scss">
  .list {
    text-align: center;
    display: flex;
    flex-direction: initial;
    flex-wrap: wrap;
  }
  .search-summary {
    text-align: center;
    color: white;
    strong {
      color: red;
    }
  }
  .article-box {
    width: 100%;
    max-width: 900px;
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    
    .box-title {
      color: white;
      strong {
        color: #D24D57;
      }
    }
    .article-content {
      border-radius: 10px;
      margin: 10px auto;
      padding: 10px 0;
      width: 100%;
      display: flex;
      flex-wrap: wrap;
      transition-duration: 0.3s;;
      &:hover {
        box-shadow: 1px 1px 10px black;
        transform: translateY(-5px);
      }
      .left-content, .right-content {
        position: relative;
        width: 100%;
        padding-left: 15px;
        padding-right: 15px;
      }
      .left-content {
        padding-left: 10px;
        flex: 0 0 16.6666667%;
        max-width: 16.6666667%;
        img {
          height: auto;
          width: 100%;
          border-radius: 10px;
          vertical-align: middle;
          border-style: none;
        }
      }
      .right-content {
        flex-basis: 0;
        flex-grow: 1;
        min-width: 0;
        max-width: 100%;
        color: white;
        font-family: "微软雅黑", "黑体", "宋体";
        .post-title {
          font-size: 24px;
          &:hover {
            text-decoration: underline;
            cursor: pointer;
          }
        }
      }
    }
    .highlight {
      color: yellow;
    }
  }
</style>