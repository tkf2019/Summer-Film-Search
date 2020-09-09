<script>
  export default {
    name: 'styleButton',
    props: {
      colorStyle: {
        type: String,
        required: true 
      }
    },
    render(h) {
      return h('div',{
        class: 'button-pack-' + this.colorStyle
      }, [
        h('button', {
          class: {
            'color-button': true
          },
          on: {
            click: () => {
              document.getElementsByTagName('body')[0].className = this.colorStyle
            } 
          }
        })
      ])
    }
  }
</script>

<style lang="scss">
  .button-pack {
    align-self: center;
  }
  .color-button {
    vertical-align: middle;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    outline: none;
    border: none;
    margin: 10px 5px;
    transition-duration: 0.3s;
    cursor: pointer;
    &:hover {
      transform: scale(1.2, 1.2);
      -webkit-filter:brightness(1.5);
      -o-filter:brightness(1.5);
      -moz-filter:brightness(1.5);
      filter:brightness(1.5);
    }
  }
</style>