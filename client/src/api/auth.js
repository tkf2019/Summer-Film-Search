import instance from './index'

export default {
  getTotal(keys, type, packSize, packIndex) {
    return instance.get('/search/', {
      params: {
        keys,
        type,
        packSize,
        packIndex
      }
    })
  },
  getMovieInfo(id, type) {
    return instance.get('/info/', {
      params: { id, type }
    })
  },
  getStarInfo(id, type) {
    return instance.get('/info/', {
      params: { id, type }
    })
  }
}
