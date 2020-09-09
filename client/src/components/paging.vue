<script>
import { mapState } from 'vuex'
export default {
  name: 'Paging',
  data() {
    return {
      pagePack: 1,
      inputValue: ''
    } 
  },
  render(h) {
    let pageList = []
    const articleNumber = this.searchData.number
    const pageNumber= Math.ceil(articleNumber / 16)
    const maxPagePack = Math.ceil(pageNumber / 5)
    
    if (this.pagePack != 1) {
      pageList.push(h('li', {
        class: 'page-button'
      }, [
        h('a', {
          domProps: {
            innerHTML: '1'
          },
          on: {
            click: () => {
              this.pagePack = 1
              this.$emit('changePage', 1)
            }
          }
        })
      ]))
      pageList.push(h('li', {
        class: 'page-button'
      }, [
        h('a', {
          domProps: { 
            innerHTML: `...`
          },
          on: {
            click: () => {
              this.pagePack--
            }
          }
        })
      ]))
    }
    for (let i = (this.pagePack - 1) * 5; i < this.pagePack * 5 && i < pageNumber; ++i) {
      pageList.push(h('li', {
        class: 'page-button'
      }, [
        h('a', {
          domProps: {
            innerHTML: `${i + 1}`
          },
          on: {
            click: () => {
              this.$emit('changePage', i + 1)
            }
          }
        })
      ]))
    }
    if (this.pagePack < maxPagePack) {
      pageList.push(h('li', {
        class: 'page-button'
      }, [
        h('a', {
          domProps: {
            innerHTML: `...`
          },
          on: {
            click: () => {
              this.pagePack++
            }
          }
        })
      ]))
      pageList.push(h('li', {
        class: 'page-button'
      }, [
        h('a', {
          domProps: {
            innerHTML: `${pageNumber}`
          },
          on: {
            click: () => {
              this.pagePack = maxPagePack
              this.$emit('changePage', pageNumber)
            }
          }
        })
      ]))
    }
    pageList.push(h('li', {
      class: 'page-button'
    }, [
      h('a', {
        domProps: {
          innerHTML: `Jump to`
        },
        on: {
          click: () => {
            if (this.inputValue < pageNumber) {
              this.pagePack = Math.ceil(this.inputValue / 5)
              this.$emit('changePage', this.inputValue)
            }
          }
        }
      })
    ]))
    pageList.push(h('input', {
      domProps: {
        value: this.inputValue 
      },
      on: {
        input: event => {
          this.inputValue = event.target.value
        }
      }
    }))
    
    return h('ul', {
      class: 'page-buttons'
    }, pageList)
  },
  computed: mapState('search', [
    'searchData'
  ])
}
</script>

<style lang="scss">
  .page-buttons {
    width: auto;
    margin: 0 auto;
    display: inline-block;
    align-self: center;
    bottom: 50px;
    color: white;
    height: 20px;
    justify-content: center!important;
    display: flex;
    padding-left: 0;
    list-style: none;
    margin-bottom: 1rem;

    input {
      width: 50px;
      height: 30px;
      font-size: 16px;
      outline: none;
      border-radius: 10px;
      padding-left: 5px;
      padding-right: 5px;
      margin-top: 16px;
    }
  }
  .page-button {
    margin: 20px 20px;
    font-size: 20px;
    transition-duration: 0.3s;
    &:hover {
      color: yellow;
      transform: scale(1.2, 1.2);
      cursor: pointer;
    }
  }
</style>