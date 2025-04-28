<template>
    <div class="max-w-7xl mx-auto grid grid-cols-5 gap-4">

        <div class="main-middle col-span-3 space-y-4">
            <div class="p-4 bg-white border border-gray-200 rounded">
                <form @submit.prevent="handleSubmit">
                    <div class="p-4">
                        <textarea class="bg-gray-100 w-full rounded-lg p-3 focus:outline-gray-100 focus:shadow-md focus:bg-white" rows="3" placeholder="What are you thinking about?" v-model="postStore.postPayload.body"></textarea>
                    </div>
                    <div class="p-4 flex justify-between items-center mb-2 border-t border-gray-200">
                        <button type="button" class="btn-lg-secondary">Attach Image</button>
                        <button type="submit" class="btn-lg-primary">Post</button>
                    </div>
                </form>
            </div>
            <div v-for="post in postList" :key="post.id">
                <FeedItem :post="post"/>
            </div>
        </div>
        <div class="main-right col-span-2">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>

<script setup lang="ts">
import FeedItem from '@/components/FeedItem.vue';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import { usePostStore } from '@/stores/posts';
import { storeToRefs } from 'pinia';
import { onMounted, ref, reactive } from 'vue';

const postStore = usePostStore();

const { postList } = storeToRefs(postStore);

onMounted( async() => {
    await postStore.fetchPostList();
})

const handleSubmit = async() => {
    await postStore.createPost();
}
</script>