<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="">
            <div class="p-12 bg-white border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Signup</h1>

                <p class="mb-6 text-gray-500">Lorem ipsum dolor sit amet consectetur adipisicing elit. Nisi quidem et sequi in consectetur ea, eveniet repellendus. Minus, illo harum. Optio cum sunt ad molestiae eveniet veritatis quae inventore veniam.</p>

                <p class="font-bold">
                   Already have an account? <RouterLink to="/login" class="underline">Click Here</RouterLink>
                </p>
            </div>
        </div>
        <div class="">
            <div class="p-12 bg-white border-gray-200 rounded-lg">
                <form class="space-y-6"  @submit.prevent="submitForm">
                    <div>
                        <label>Email</label><br/>
                        <input type="text" placeholder="Your e-mail address" class="border border-gray-200 rounded-lg px-3 py-1 shadow-md focus:shadow-lg focus:outline-none w-full mt-4" v-model="form.email"/>
                    </div>
                    <div>
                        <label>Name</label><br/>
                        <input type="text" placeholder="Your full name" class="border border-gray-200 rounded-lg px-3 py-1 shadow-md focus:shadow-lg focus:outline-none w-full mt-4" v-model="form.name"/>
                    </div>
                    <div>
                        <label>Password</label><br/>
                        <input type="password" placeholder="Password" class="border border-gray-200 rounded-lg px-3 py-1 shadow-md focus:shadow-lg focus:outline-none w-full mt-4" v-model="form.password"/>
                    </div>
                    <div>
                        <label>Repeat Password</label><br/>
                        <input type="password" placeholder="Repeat Password" class="border border-gray-200 rounded-lg px-3 py-1 shadow-md focus:shadow-lg focus:outline-none w-full mt-4" v-model="form.password2"/>
                    </div>
                    <template v-if="form.errors">
                        <div class="bg-red-300 text-white rounded-lg"></div>
                        <span v-for="error in form.errors" :key="error">{{ error }}</span>
                    </template>
                    <div>
                        <button type="submit" class="w-full bg-purple-500 py-2 rounded-lg text-white text-xl mt-4 hover:bg-purple-700">Signup</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useToastStore } from '@/stores/toast';
import axios from 'axios';
import { reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const toastStore = useToastStore()

const form = reactive({
        email: '',
        name: '',
        password: '',
        password2: '',
})

const errors = reactive({
    name: null,
    email: null,
    password: null,
    password2: null
})

const submitForm = () => {
    let isValid = true;

    Object.keys(errors).forEach(key => {
        errors[key] = null
    })

    if(form.name === '') {
        errors.name = 'Your name is missing'
        isValid = false
    }

    if(form.password === '') {
        errors.password = 'Your password is missing'
        isValid = false
    }

    if(form.password !== form.password2) {
        errors.password2 = "Your passwords don't match"
        errors.password = "Your passwords don't match"
        isValid = false
    }

    console.log(errors)
    if(isValid) {
        axios
        .post('/api/account/signup/', form)
        .then((response) => {
            console.log(response.data)
            if(response.data) {
                toastStore.showToast(5000, "You have successfully registered.", 'bg-emerald-400')
                router.push('/login')
            } else {
                toastStore.showToast(5000, "Something went wrong! Please try again", "bg-red-400")
                
                form.password = ''
                form.password2 = ''
            }
        })
        .catch(error => {
            console.log('error', error)
        })
    }
}
</script>