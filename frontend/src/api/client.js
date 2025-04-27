import axios from 'axios';
import router from '@/router';
import jwtServices from '@/services/jwt';
import { authAPI } from '@/core/endpoints';

const apiUrl = 'http://localhost:8000/api/'

const apiClient = axios.create({
  baseURL: apiUrl,
  headers: {
    'Content-Type': 'application/json'
  }
})

apiClient.interceptors.request.use((config) => {
  const token = jwtServices.getToken()
  if (token) {
    config.headers['Authorization']= `Bearer ${token}`
  }
  return config
},
(error) => {
  return Promise.reject(error)
})

apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async function (error){ 
    const {
      config, 
      response: {status}
    } = error
    const originalRequest = config
    const refreshToken = jwtServices.getRefreshToken()
    if (status === 401 && !originalRequest._retry && refreshToken) {
      originalRequest._retry = true
      try {
        const response = await axios.post(apiUrl + authAPI.refresh, {
          refresh: refreshToken
        })
        const token = response.data.access
        jwtServices.setToken(token)
        originalRequest.headers['Authorization'] = `Bearer ${token}`
        return await axios(originalRequest)
      } catch (e){
        jwtServices.destroyToken()
        router.push({ name: 'login'})
        console.error('Token refresh failed', e)
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient;