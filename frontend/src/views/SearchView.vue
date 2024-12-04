<script setup lang="ts">
    import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
    import Trends from '@/components/Trends.vue';
    import { ref } from 'vue';
    import axios from 'axios';
import FeedItem from '@/components/FeedItem.vue';

    const searchQuery = ref('')

    const searchedUsers = ref(null)

    const searchedPosts = ref(null)

    const handleSearch = async() => {
        await axios
        .get(`/api/posts/search?q=${searchQuery.value}`)
        .then(response => {
            searchedUsers.value = response.data.user
            searchedPosts.value = response.data.posts
            console.log(searchedUsers.value)
        })
    }

</script>

<template>
    <div class="grid grid-cols-4">
        <div class="col-span-3">
            <div class="bg-white p-3 rounded-lg mb-6">
                <div class="flex justify-between">
                    <input v-model="searchQuery" type="text" placeholder="What are you looking for"
                        class="bg-white px-3 py-2 w-full rounded-lg border border-gray-200">
                    <div class="flex">
                        <button class="bg-purple-500 hover:bg-purple-700 px-3 py-2 mx-3 rounded-lg text-white" @click="handleSearch">
                            <span class="text-xs flex space-x-2 items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-4">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                                </svg>
                                <p>Search</p>
                            </span>
                        </button>
                    </div>
                </div>
            </div>

            <div v-if="searchedUsers" class="bg-white p-3 rounded-lg mb-6 border border-gray-200">
                <div class="grid grid-cols-4">
                    <div v-for="(user, index) in searchedUsers" :key="index" class="col-span-1">
                        <div class="p-4 bg-gray-200 border m-2 border-gray-200 rounded-lg text-center">
                            <RouterLink :to="{name: 'profile', params:{ id:user.id }}">
                                <img :src="user.avatar" class="rounded-full m-auto"/>
                            </RouterLink>
                            <p class="mt-4 text-xl font-semibold">{{ user.name }}</p>

                            <div class="mt-6 flex space-x-8 justify-around">
                                <p class="text-xs text-gray-500">{{user.friends_count}} friends</p>
                                <p class="text-xs text-gray-500">{{user.post_count}} posts</p>
                            </div>
                        </div>
                    </div>
                    
                </div>
            </div>
            <div v-if="searchedPosts">
                <div v-for="(post, index) in searchedPosts" :key="index">
                    <FeedItem :post="post"/>
                </div>
            </div>

        </div>
        <div class="col-span-1">
            <div class="ml-6">
                <PeopleYouMayKnow />
                <Trends />
            </div>
        </div>
    </div>
</template>