<template>
    <div class="p-4 mb-6 rounded-lg primary-border">
        <p class="text-xl font-semibold">People You May Know</p>
        <div class="">
            <ul>
                <li class="py-2 rounded-md border-stone-200 dark:border-stone-700"
                v-for="user,index in userRecommendations" :key="index" :class="index+1 === userRecommendations.length ? `border-none` : 'border-b'">
                    <div class="flex justify-between items-center space-x-2 ">
                        <img :src="user.avatar"
                            class="rounded-full h-10 w-10" />
                        <p class="truncate ... font-semibold">{{ user.name }}</p>
                        <RouterLink :to="{ name: 'profile', params: { id:user.id }}">
                            <button class="btn-primary">Show</button>
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