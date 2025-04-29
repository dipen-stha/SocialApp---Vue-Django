<template>
  <div class="max-w-7xl mx-auto grid grid-cols-5 gap-4">
    <div class="main-middle col-span-3 space-y-4">
      <div class="p-4 border border-stone-200 dark:border-stone-700 rounded">
        <form @submit.prevent="handleSubmit">
          <div class="p-4">
            <textarea
              class="bg-white dark:bg-stone-800 appearance-none w-full rounded-lg p-3 focus:outline-stone-500 focus:shadow-md focus:bg-gray-50 dark:focus:bg-stone-700"
              rows="3"
              placeholder="What are you thinking about?"
              v-model="postStore.postPayload.body"
              required
            ></textarea>
          </div>
          <div
            class="p-4 flex justify-between items-center mb-2 border-t border-stone-200 dark:border-stone-700"
          >
            <button type="button" class="btn-secondary">Attach Image</button>
            <button type="submit" class="btn-primary">Post</button>
          </div>
        </form>
      </div>
      <div v-for="post in postList" :key="post.id">
        <FeedItem :post="post" />
      </div>
    </div>
    <div class="main-right col-span-2">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>

<script setup lang="ts">
import FeedItem from "@/components/FeedItem.vue";
import PeopleYouMayKnow from "@/components/PeopleYouMayKnow.vue";
import Trends from "@/components/Trends.vue";
import { usePostStore } from "@/stores/posts";
import { storeToRefs } from "pinia";
import { onMounted, ref, reactive } from "vue";

const postStore = usePostStore();

const { postList } = storeToRefs(postStore);

onMounted(async () => {
  await postStore.fetchPostList();
});

const handleSubmit = async () => {
  await postStore.createPost();
};
</script>
