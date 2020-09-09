import axios from 'axios'

const instance = axios.create({
  baseURL: '/api',
  timeout: 5000
})

instance.defaults.headers.post['Content-Type'] = 'application/json'

export default instance