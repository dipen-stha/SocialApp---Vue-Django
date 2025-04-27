import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import Vue3Toastify from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import apiClient from '@/api/client'
import initRouter from './utils/setup/routerSetup'

const app = createApp(App)

app.use(createPinia());

initRouter(app);

app.use(Vue3Toastify, {
  autoClose: 3000,
  position: 'bottom-right',
})

app.directive('click-outside', {
  beforeMount(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
})

app.config.globalProperties.$api = apiClient

app.mount('#app')