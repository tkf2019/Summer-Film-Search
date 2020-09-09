import auth from '@/api/auth'

import {
  SEARCH_BEGIN,
  SEARCH_CLEAR,
  SEARCH_FAILURE,
  SEARCH_SUCCESS
} from './types'

const state = {
  searchCompleted: false,
  searchError: false,
  searchLoading: false,
  searchData: {
    time: '',
    number: '',
    results: []
  },
  movieInfo: {
    id: '',
    name: '',
    image: '',
    score: '',
    director: [],
    author: [],
    actor: [],
    genre: [],
    location: '',
    language: '',
    date: '',
    time: '',
    description: [],
    comment: []
  },
  starInfo: {
    id: '',
    name: '',
    image: '',
    gender: '',
    birthDeath: '',
    place: '',
    occupation: '',
    movie: [],
    description: '',
    cooperator: []
  }
}

const actions = {
  getTotal ({ commit }, {keys, type, packSize, packIndex}) {
    commit(SEARCH_BEGIN)
    return auth.getTotal(keys, type, packSize, packIndex)
      .then(response => {
        commit(SEARCH_SUCCESS)
        state.searchData = response.data
      })
      .catch(() => SEARCH_FAILURE)
  },
  getMovieInfo({ commit }, {id ,type}) {
    commit(SEARCH_BEGIN)
    return auth.getMovieInfo(id, type)
      .then(response => {
          state.movieInfo = response.data
      })
      .catch(() => SEARCH_FAILURE)
  },
  getStarInfo({ commit }, {id, type}) {
    commit(SEARCH_BEGIN)
    return auth.getStarInfo(id, type)
      .then(response => {
        state.starInfo = response.data
      })
      .catch(() => SEARCH_FAILURE)
  },
  clearSearchStatus ({ commit }) {
    commit(SEARCH_CLEAR)
  }
}

const mutations = {
  [SEARCH_BEGIN] (state) {
    state.searchLoading = true
  },
  [SEARCH_CLEAR] (state) {
    state.searchCompleted = false
    state.searchError = false
    state.searchLoading = false
  },
  [SEARCH_FAILURE] (state) {
    state.searchError = true
    state.searchLoading = false
  },
  [SEARCH_SUCCESS] (state) {
    state.searchCompleted = true
    state.searchError = false
    state.searchLoading = false
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
}