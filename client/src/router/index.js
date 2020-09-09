import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'
import {mapActions} from 'vuex'

const originalReplace = VueRouter.prototype.replace
VueRouter.prototype.replace = function replace(location) {
  return originalReplace.call(this, location).catch(err => err)
}
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const Home = import('@/views/Home')
const Search = import('@/views/Search')
const List = import('@/views/List')
const MovieInfo = import('@/views/MovieInfo')
const StarInfo = import('@/views/StarInfo')
Vue.use(VueRouter)

const routes = [
  { 
    path: '/',
    redirect: '/home'
  }, {
    path: '/home',
    name: 'Home',
    component: () => Home,
    children: [
      {
        path: 'search',
        name: 'Search',
        component: () => Search
      }, {
        path: 'list',
        name: 'List',
        component: () => List
      }, {
        path: 'movie',
        name: 'MovieInfo',
        component: () => MovieInfo
      }, {
        path: 'star',
        name: 'StarInfo',
        component: () => StarInfo
      }
    ]
  }, {
    name: 'Lost',
    path: '*'
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior(to, from, savePosition) {
    return {
      x: 0,
      y: 0
    }
  }//keep the scroll part at the top
})

router.beforeEach((to, from, next) => {
  document.title = to.matched[0].name
  next()
})

export default router
