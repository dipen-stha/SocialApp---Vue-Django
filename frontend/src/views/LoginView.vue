<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="">
            <div class="p-12 bg-white border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Login</h1>

                <p class="mb-6 text-gray-500">Lorem ipsum dolor sit amet consectetur adipisicing elit. Nisi quidem et sequi in consectetur ea, eveniet repellendus. Minus, illo harum. Optio cum sunt ad molestiae eveniet veritatis quae inventore veniam.</p>

                <p class="font-bold">
                   Don't have an account? <RouterLink to="/signup" class="underline">Click Here</RouterLink>
                </p>
            </div>
        </div>
        <div class="">
            <div class="p-12 bg-white border-gray-200 rounded-lg">
                <form class="space-y-6" @submit.prevent="handleLogin">
                    <div>
                        <label>Email</label><br/>
                        <input type="text" placeholder="Your e-mail address" class="border border-gray-200 rounded-lg px-3 py-1 shadow-md focus:shadow-lg focus:outline-none w-full mt-4" v-model="form.email"/>
                        <div v-if="errors.email" class="text-red-500 px-2">{{ errors.email }}</div>
                    </div>
                    <div>
                        <label>Password</label><br/>
                        <input type="password" placeholder="Password" class="border border-gray-200 rounded-lg px-3 py-1 shadow-md focus:shadow-lg focus:outline-none w-full mt-4" v-model="form.password"/>
                        <div v-if="errors.password" class="text-red-500 px-2">{{ errors.password }}</div>
                    </div>
                    <div>
                        <button type="submit" class="bg-purple-500 hover:bg-purple-700 py-2 text-xl rounded-lg shadow-md hover:shadow-lg text-white mt-4 w-full">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { reactive } from 'vue';
import { useRouter } from 'vue-router';

const form = reactive({
    email: '',
    password: ''
})

const errors = reactive({
    email: null,
    password: null
})

const userStore = useUserStore()

const router = useRouter()

const handleLogin = async() => {
    let isValid = true;
    Object.keys(errors).forEach(key => {
        errors[key] = null
    })

    if (form.email === ''){
        errors.email = "Email is required"
        isValid = false
    }

    if (form.password === ''){
        errors.password = "Password is required"
        isValid = false
    }

    if(isValid){
        await axios
            .post('api/account/login/', form)
            .then(response => {
                if(response.data){
                    userStore.setToken(response.data)

                    axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                }
            })
            .catch(error => {
                console.log('error', error)
            })
        await axios
            .get('api/user/')
            .then(response => {
                if(response.data){
                    userStore.setUserInfo(response.data[0])
                    router.push('/feed')
                }
            })
            .catch(error => {
                console.log('error', error)
            })
    }

}

</script>