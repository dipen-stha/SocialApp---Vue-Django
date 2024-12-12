import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import axios from 'axios'
import Cookies from 'js-cookie'

axios.defaults.baseURL = 'http://localhost:8000'

if (Cookies.get('access')){
    axios.defaults.headers.common['Authorization'] = `Bearer ${Cookies.get('access')}`
}
const app = createApp(App)

app.use(createPinia())
app.use(router, axios)

app.mount('#app')
