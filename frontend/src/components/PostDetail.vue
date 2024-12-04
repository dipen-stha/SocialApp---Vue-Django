<template>
    <div class="p-3 bg-white m-3 border border-gray-200 rounded-lg">
        <div class="flex justify-between items-center flex-x-4 w-full">
            <div class="flex space-x-2">
                <img :src="postDetail.created_by.avatar" class="rounded-full h-10 w-10" />
                <p class="text-xl font-semibold">{{ postDetail.created_by.name }}</p>
            </div>
            <div class="">
                <p class="text-gray-500">{{ postDetail.created_at_formatted }}</p>
            </div>
        </div>
        <div class="p-3">
            <p>{{ postDetail.body }}</p>
        </div>
        <div class="my-6 flex justify-between">
            <div class="flex space-x-6">
                <div class="flex items-center space-x-2">
                    <button @click="handleLike" class="cursor-pointer hover:scale-125">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                        </svg>
                    </button>
                    <span class="text-gray-500 text-xs">{{ postDetail.likes_count }} likes</span>
                </div>
                <div class="flex items-center space-x-2">
                    <button>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 0 1-.923 1.785A5.969 5.969 0 0 0 6 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337Z" />
                        </svg>
                    </button>
                    <span class="text-gray-500 text-xs">{{ postDetail.comments_count }} comments</span>
                </div>
            </div>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                </svg>
            </div>
        </div>

        <div>
            <div>
                <form @submit.prevent="handleComment">
                    <div class="flex space-x-2 items-center">
                        <textarea class="w-full bg-gray-100 rounded-md px-3 py-2 outline-none"
                            :class="{ 'outline-red-600': isEmpty }" v-model="body"
                            placeholder="Write your comment"></textarea>
                        <button type="submit"
                            class="px-3 py-2 bg-emerald-500 hover:bg-emerald-700 rounded-lg text-gray-100">Comment</button>
                    </div>
                </form>
            </div>
            <div class="border-b my-3">
                <h1 class="text-xl font-semibold">Comments</h1>
            </div>
            <div>
                <div v-for="comment in postDetail.comments" :key="comment.id"
                    class="flex space-x-3 bg-gray-100 items-center mb-4 rounded-lg">
                    <img :src="comment.created_by.avatar" class="rounded-full h-10 w-10" />
                    <div class="">
                        <h1 class="font-semibold text-gray-800">{{ comment.created_by.name }}</h1>
                        <p class="gray-800">{{ comment.body }}</p>
                    </div>
                    <div class="grow text-end pr-2">
                        <p>{{ comment.created_at_formatted }} ago</p>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

const props = defineProps({
    postDetail: Object
})

const body = ref(null)

const isEmpty = ref(false)

const handleComment = async () => {
    if (body.value !== null | '') {
        try {
            const response = await axios.post(`/api/posts/${props.postDetail.id}/add_comments/`, {
                'body': body.value
            })
            isEmpty.value = false
            props.postDetail.comments.unshift(response.data.comment);
            props.postDetail.comments_count += 1
            body.value = null

        } catch (error) {
            console.error('Error posting comment:', error);
        }
    } else {
        isEmpty.value = true
    }
}
</script>