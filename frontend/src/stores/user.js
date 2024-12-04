import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";
import { reactive } from "vue";

export const useUserStore = defineStore('user', () => {

    const user = reactive({
        isAuthenticated: false,
        id: null,
        name: null,
        email: null,
        access: null,
        refresh: null,
    })

    const initStore = () => {
        if (Cookies.get('user.access')) {
            user.access = Cookies.get('user.access')
            user.refresh = Cookies.get('user.refresh')
            user.id = Cookies.get('user.id')
            user.email = Cookies.get('user.email')
            user.name = Cookies.get('user.name')
            user.isAuthenticated = true

            refreshToken()
        }
    }

    const setToken = (data) => {

            user.access = data.access
            user.refresh = data.refresh
            user.isAuthenticated = true

            Cookies.set('user.access', data.access)
            Cookies.set('user.refresh', data.refresh)
        }

    const removeToken = () => {

            user.refresh = null
            user.access = null
            user.isAuthenticated = null
            user.id = null
            user.name = null
            user.email = null

            Cookies.set('user.access', '')
            Cookies.set('user.refresh', '')
            Cookies.set('user.id', '')
            Cookies.set('user.name', '')
            Cookies.set('user.email', '')
        }

    const setUserInfo = (user) => {

            user.id = user.id
            user.name = user.name
            user.email = user.email
            Cookies.set('user.id', user.id)
            Cookies.set('user.name', user.name)
            Cookies.set('user.email', user.email)
        }

    const refreshToken = () => {
            axios.post('/api/refresh/', {
                refresh: user.refresh
            })
            .then((response) => {
                user.access = response.data.access

                Cookies.set('user.access', response.data.access)

                axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
            })
            .catch((error) => {
                console.log(error)

                removeToken()
            })
        };
        return {
            user,
            initStore,
            setToken,
            removeToken,
            setUserInfo,
            refreshToken
        }
    })