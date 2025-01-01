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

app.directive('click-outside', {
    beforeMount: function (element, binding) {
        console.log({
            element,
            binding
        });
        element.clickOutsideEvent = function (event) {
            if (!(element === event.target || element.contains(event.target)) && typeof binding.value === 'function') {
                binding.value(event);
            }
        };
        document.body.addEventListener('click', element.clickOutsideEvent)
    },
    unmounted: function (element) {
        document.body.removeEventListener('click', element.clickOutsideEvent)
    }
});
app.mount('#app')

