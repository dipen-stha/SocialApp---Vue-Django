<template>
    <div class="bg-white p-4 mb-6 rounded-lg border border-gray-200">
        <p class="text-xl font-semibold">People You May Know</p>
        <div class="my-4">
            <ul>
                <li class="mb-4"
                v-for="user,index in userRecommendations" :key="index">
                    <div class="flex justify-between items-center space-x-2">
                        <img :src="user.avatar"
                            class="rounded-full h-10 w-10" />
                        <p class="truncate ... font-semibold">{{ user.name }}</p>
                        <RouterLink :to="{ name: 'profile', params: { id:user.id }}">
                            <button class="bg-purple-500 hover:bg-purple-700 px-2 py-1 rounded-lg text-gray-100 hover:text-white">Show</button>
                        </RouterLink>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import apiClient from "@/api/client";
import { useUserStore } from "@/stores/user/user";
import { storeToRefs } from "pinia";
import { onMounted, ref } from 'vue';

const users = ref([])

const userStore = useUserStore();

const { userRecommendations } = storeToRefs(userStore);

onMounted(() => {
    userStore.fetchUserRecommendations();
})

</script>