<script setup lang="ts">
import FeedItem from '@/components/FeedItem.vue';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import axios from 'axios';
import { onMounted, ref, reactive } from 'vue';

onMounted(() => {
    getFeed()
})

const posts = ref([])

const content = reactive({
    body: '',
    attachments: []
})

const handleSubmit = async() => {
    await axios
    .post('/api/posts/', content)
    .then(response => {
        posts.value.unshift(response.data)
    })
}

const getFeed = async() => {
    await axios
    .get('/api/posts/')
    .then(response => {
        posts.value = response.data.posts
    })
    .catch(error => {
        console.log(error)
    })
}
</script>

<template>
    <div class="max-w-7xl mx-auto grid grid-cols-5 gap-4">

        <div class="main-middle col-span-3 space-y-4">
            <div class="p-4 bg-white border border-gray-200 rounded">
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
            <FeedItem :posts="posts"/>
        </div>
        <div class="main-right col-span-2">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>