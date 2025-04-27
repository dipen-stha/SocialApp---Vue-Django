<script setup lang="ts">
import FeedItem from '@/components/FeedItem.vue';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import { useUserStore } from '@/stores/user/user';
import axios from 'axios';
import { onMounted, ref, reactive, watch } from 'vue';
import { useRoute } from 'vue-router';

onMounted(() => {
    if (route.params.id) {
        determineRelationshipState()
    }
})

const posts = ref([])
const user = ref(null)

const route = useRoute()

const userStore = useUserStore()

const content = reactive({
    body: '',
    attachments: []
})

const friendRequest = ref(null)

const isFriend = ref(false)

const hasRequest = ref(false)

const relationshipState = ref('')

const handleSubmit = async () => {
    await axios
        .post('/api/posts/', content)
        .then(response => {
            posts.value.unshift(response.data)
            content.body = ''
        })
}

const determineRelationshipState = async () => {
    try {
        const userResponse = await axios.get(`/api/posts?user=${route.params.id}`)
        user.value = userResponse.data.user;
        posts.value = userResponse.data.posts;

        const friendRequestResposne = await axios.get('/api/friend-requests/')
        const requests = friendRequestResposne.data

        const currentUserId = userStore.user.id;
        const sentRequest = requests.find(item => item.created_for.id === route.params.id && item.created_by.id === currentUserId);
        const receivedRequest = requests.find(item => item.created_by.id === route.params.id && item.created_for.id === currentUserId);
        if (user.value.friends.find(item => item.friend === currentUserId)) {
            relationshipState.value = 'friends';
            isFriend.value = true;
        } else if (sentRequest) {
            relationshipState.value = 'request_sent';
            friendRequest.value = sentRequest;
        } else if (receivedRequest) {
            relationshipState.value = 'request_received';
            friendRequest.value = receivedRequest;
            hasRequest.value = true;
        } else {
            relationshipState.value = 'not_friends';
        }
    } catch (error) {
        console.log(error)
    }


}

const sendRequest = async () => {
    try {
        const response = await axios.post(`/api/friend-requests/`, {
            "created_for": route.params.id
        });
        friendRequest.value = response.data;
        relationshipState.value = 'request_sent';
    } catch (error) {
        console.error(error);
    }
}

const handleRequest = async (status: string) => {
    try {
        const response = await axios.put(`/api/friend-requests/${friendRequest.value.id}/`, {
            "status": status
        });
        if (status === 'accepted') {
            relationshipState.value = 'friends';
            isFriend.value = true;
        } else {
            relationshipState.value = 'not_friends';
            hasRequest.value = false;
        }
        friendRequest.value = null; // Clear request object
    } catch (error) {
        console.error(error);
    }
}


watch(() => route.params, () => {
    determineRelationshipState()
})
</script>

<template>
    <div v-if="user" class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 rounded-lg text-center">
                <img :src="user.avatar" class="rounded-full m-auto w-15 h-15" />
                <p class="mt-4 text-xl font-semibold">{{ user.name }}</p>
                <p>{{ user.email }}</p>
                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{ name: 'friends', params: { id: user.id } }">
                        <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                    </RouterLink>
                    <p class="text-xs text-gray-500">{{ posts.length }} posts</p>
                </div>
                <div v-if="userStore.user?.id !== route.params.id" class="">
                    <div v-if="relationshipState === 'friends'" class="flex flex-wrap gap-y-2">
                        <button class="bg-emerald-500 hover:bg-emerald-600 px-2 py-2 rounded-lg mt-4 text-white w-1/2">
                            <span class="flex space-x-2 text-xs">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                                </svg>
                                <p>
                                    Friends
                                </p>
                            </span>
                        </button>
                        <button class="bg-red-500 hover:bg-red-600 px-2 py-2 rounded-lg mt-4 text-white w-1/2">
                            <span class="flex space-x-2 text-xs">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-4">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M22 10.5h-6m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM4 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 10.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                                </svg>
                                <p>
                                    Unfriend
                                </p>
                            </span>
                        </button>
                        <button class="py-1 px-2 bg-blue-500 hover:bg-blue-700 w-full rounded-lg ">
                            <span class="text-white">
                                Message
                            </span>
                        </button>
                    </div>

                    <div v-else-if="relationshipState === 'request_sent'" class="">
                        <button @click=""
                            class="bg-gray-500 hover:bg-gray-700 px-3 py-2 rounded-lg mt-4 w-full text-white">
                            <span class="flex space-x-4">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                                </svg>
                                <p>
                                    Request Sent
                                </p>
                            </span>
                        </button>
                    </div>
                    <div v-else-if="relationshipState === 'not_friends'" class="">
                        <button @click="sendRequest"
                            class="bg-purple-500 hover:bg-purple-700 px-3 py-2 rounded-lg mt-4 w-full text-white">
                            <span class="flex space-x-4">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                                </svg>
                                <p>
                                    Add Friend
                                </p>
                            </span>
                        </button>
                    </div>
                    <div v-else-if="!isFriend && hasRequest" class="flex space-x-2 justify-center text-center">
                        <button class="bg-emerald-500 hover:bg-emerald-600 px-2 py-2 rounded-lg mt-4 text-white w-1/2"
                            @click="handleRequest('accepted')">
                            <span class="flex space-x-2 text-xs">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                                </svg>
                                <p class="hidden md:block">
                                    Accept
                                </p>
                            </span>
                        </button>
                        <button
                            class="bg-red-500 hover:bg-red-600 px-2 py-2 rounded-lg mt-4 text-white w-1/2 text-center"
                            @click="handleRequest('rejected')">
                            <span class="flex space-x-2 text-xs text-center">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-4">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M22 10.5h-6m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM4 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 10.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                                </svg>
                                <p class="hidden md:block">
                                    Reject
                                </p>
                            </span>
                        </button>
                    </div>

                </div>
            </div>
        </div>
        <div class="main-middle col-span-2 space-y-4">
            <div v-if="userStore.user.id === user.id" class="p-4 bg-white border border-gray-200 rounded">
                <form @submit.prevent="handleSubmit">
                    <div class="p-4">
                        <textarea class="bg-gray-100 w-full rounded-lg p-3" rows="3"
                            placeholder="What are you thinking about?" v-model="content.body"></textarea>
                    </div>
                    <div class="p-4 flex justify-between items-center mb-2 border-t border-gray-200">
                        <button type="button"
                            class="px-3 py-2 bg-gray-400 hover:bg-gray-500 rounded-lg shadow-md hover:shadow-lg font-semibold text-gray-100 hover:text-white">Attach
                            Image</button>
                        <button type="submit"
                            class="px-3 py-2 bg-purple-500 hover:bg-purple-700 rounded-lg shadow-md hover:shadow-lg font-semibold text-gray-100 hover:text-white">Post</button>
                    </div>
                </form>
            </div>
            <div v-for="(post, index) in posts" :key="index">
                <FeedItem :post="post" />
            </div>
        </div>
        <div class="main-right col-span-1">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>