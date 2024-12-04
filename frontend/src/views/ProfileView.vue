<script setup lang="ts">
import FeedItem from '@/components/FeedItem.vue';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { onMounted, ref, reactive, watch } from 'vue';
import { useRoute } from 'vue-router';

onMounted(() => {
    getFeed()
})

const posts = ref([])

const route = useRoute()

const userStore = useUserStore()

const content = reactive({
    body: '',
    attachments: []
})
const user = ref(null)

const handleSubmit = async() => {
    await axios
    .post('/api/posts/', content)
    .then(response => {
        posts.value.unshift(response.data)
    })
}

const getFeed = async() => {
    await axios
    .get(`/api/posts?user=${route.params.id}`)
    .then(response => {
        posts.value = response.data.posts
        user.value = response.data.user
    })
    .catch(error => {
        console.log(error)
    })
}

const sendRequest = async() => {
    await axios
    .post(`api/friends/?user=${user.value.id}`)
    .then(response => {
        console.log(response.data)
    })
}

watch(route, () => {
    getFeed()
})
</script>

<template>
    <div v-if="user" class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 rounded-lg text-center">
                <img :src="user.avatar" class="rounded-full m-auto"/>
                <p class="mt-4 text-xl font-semibold">{{ user.name }}</p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{name:'friends', params:{id: user.id}}">
                        <p class="text-xs text-gray-500">{{user.friends_count}} friends</p>
                    </RouterLink>
                    <p class="text-xs text-gray-500">{{ posts.length }} posts</p>
                </div>

                <div v-if="userStore.user.id !== route.params.id && !(user.friends.includes(userStore.user.id))" class="">
                    <button @click="sendRequest" class="bg-purple-500 hover:bg-purple-700 px-3 py-2 rounded-lg mt-4 w-full text-white">
                        <span class="flex space-x-4">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                            </svg>
                            <p>
                            Add Friend
                            </p>
                        </span>
                    </button>
                </div>
                <div v-else-if="user.friends.includes(userStore.user.id)" class="flex space-x-4">
                    <button class="bg-emerald-500 hover:bg-emerald-600 px-2 py-2 rounded-lg mt-4 text-white">
                        <span class="flex space-x-2 text-xs">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                            </svg>
                            <p>
                            Friends
                            </p>
                        </span>
                    </button>
                    <button class="bg-red-500 hover:bg-red-600 px-2 py-2 rounded-lg mt-4 text-white">
                        <span class="flex space-x-2 text-xs">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M22 10.5h-6m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM4 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 10.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                            </svg>
                            <p>
                            Unfriend
                            </p>
                        </span>
                    </button>
                </div>
            </div>
        </div>
        <div class="main-middle col-span-2 space-y-4">
            <div v-if="userStore.user.id === user.id" class="p-4 bg-white border border-gray-200 rounded">
                <form @submit.prevent="handleSubmit">
                    <div class="p-4">
                        <textarea class="bg-gray-100 w-full rounded-lg p-3" rows="3" placeholder="What are you thinking about?" v-model="content.body"></textarea>
                    </div>
                    <div class="p-4 flex justify-between items-center mb-2 border-t border-gray-200">
                        <button type="button" class="px-3 py-2 bg-gray-400 hover:bg-gray-500 rounded-lg shadow-md hover:shadow-lg font-semibold text-gray-100 hover:text-white">Attach Image</button>
                        <button type="submit" class="px-3 py-2 bg-purple-500 hover:bg-purple-700 rounded-lg shadow-md hover:shadow-lg font-semibold text-gray-100 hover:text-white">Post</button>
                    </div>
                </form>
            </div>
            <div v-for="(post,index) in posts" :key="index">
                <FeedItem :post="post" />
            </div>
        </div>
        <div class="main-right col-span-1">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>