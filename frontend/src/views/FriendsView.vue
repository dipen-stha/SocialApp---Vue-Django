<script setup lang="ts">
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { onMounted, ref, reactive, watch } from 'vue';
import { useRoute } from 'vue-router';

onMounted(() => {
    getFriends()
})

const route = useRoute()

const userStore = useUserStore()

const acceptedFriends = ref(null)
const pendingFriends = ref(null)

const content = reactive({
    body: '',
    attachments: []
})
const user = userStore.user

const status = ref('')

const handleRequest = async (status: string, id: string) => {
    await axios.put(`/api/friends/${id}/update_status/?status=${status}`)
        .then(response => {
            getFriends()
        })
        .catch(error => {
            console.log(error)
        })
}

const getFriends = async () => {
    if (user.id === route.params.id) {
        await axios
            .get(`/api/friends/`)
            .then(response => {
                acceptedFriends.value = response.data.accepted
                pendingFriends.value = response.data.sent
                console.log(pendingFriends.value)
            })
    } else {
        await axios
            .get(`api/friends/get_friends/?id=${route.params.id}`)
            .then(response => {
                acceptedFriends.value = response.data.friends
            })
    }
}

watch(route, () => {
    getFriends()
})

</script>

<template>
    <div v-if="user" class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-middle col-span-3 space-y-4">
            <div v-if="user.id === route.params.id" class="p-4 bg-white rounded border border-gray-200">
                <div class="w-full border-b pb-3">
                    <h1 class="text-3xl font-semibold">Friend Requests</h1>
                </div>
                <div class="mt-4">
                    <ul>
                        <li class="mb-4" v-for="user, index in pendingFriends" :key="index">
                            <div class="flex justify-between items-center space-x-2">
                                <div class="flex space-x-5 items-center">
                                    <img :src="user.created_by.avatar" class="rounded-full h-10 w-10" />
                                    <p class="text-xl font-semibold">{{ user.created_by.name }}</p>
                                </div>
                                <div class="flex space-x-4">
                                    <button @click="handleRequest('accepted', user.id)"
                                        class="bg-purple-500 hover:bg-purple-700 px-2 py-1 rounded-lg text-gray-100 hover:text-white">Accept</button>
                                    <button @click="handleRequest('rejected', user.id)"
                                        class="bg-red-500 hover:bg-red-700 px-2 py-1 rounded-lg text-gray-100 hover:text-white">Reject</button>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="p-4 bg-white rounded border border-gray-200">
                <div class="w-full border-b pb-3">
                    <h1 class="text-3xl font-semibold">Friends</h1>
                </div>
                <div class="mt-4">
                    <ul>
                        <li class="mb-4" v-for="user, index in acceptedFriends" :key="index">
                            <div class="flex justify-between items-center space-x-2">
                                <div class="flex space-x-4 items-center">
                                    <img :src="user.avatar" class="rounded-full h-10 w-10" />
                                    <p class="truncate ... font-semibold">{{ user.name }}</p>
                                </div>
                                <button
                                    class="bg-purple-500 hover:bg-purple-700 px-2 py-1 rounded-lg text-gray-100 hover:text-white">Show</button>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="main-right col-span-1">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>