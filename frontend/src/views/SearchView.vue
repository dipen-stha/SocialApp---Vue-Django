<template>
  <div class="grid grid-cols-4">
    <div class="col-span-3">
      <div class="bg-stone-50 dark:bg-stone-900 p-3 rounded-lg mb-6">
        <div class="flex gap-x-[5px]">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="What are you looking for"
            class="bg-stone-50 dark:bg-stone-900 px-3 py-2 w-full rounded-md border border-stone-200 dark:border-stone-700"
          />
          <div class="flex">
            <button class="btn-primary" @click="handleSearch">
              <span class="text-xs flex space-x-2 items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="size-4"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
                  />
                </svg>
                <p>Search</p>
              </span>
            </button>
          </div>
        </div>
      </div>

      <div
        v-if="searchedUsers"
        class="bg-stone-50 dark:bg-stone-900 p-3 rounded-lg mb-6 border border-stone-200 dark:border-stone-700"
      >
        <div class="grid grid-cols-4">
          <div
            v-for="(user, index) in searchedUsers"
            :key="index"
            class="col-span-1"
          >
            <div
              class="p-4 bg-stone-50 dark:bg-stone-900 border m-2 border-stone-200 dark:border-stone-700 rounded-lg text-center"
            >
              <RouterLink :to="{ name: 'profile', params: { id: user.id } }">
                <img :src="user.avatar" class="rounded-full m-auto w-10 h-10" />
              </RouterLink>
              <p class="mt-4 text-xl font-semibold">{{ user.name }}</p>

              <div class="mt-6 flex space-x-8 justify-around">
                <p class="text-xs text-stone-900 dark:text-stone-50">
                  {{ user.friends_count }} friends
                </p>
                <p class="text-xs text-stone-900 dark:text-stone-50">{{ user.post_count }} posts</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="searchedPosts">
        <div v-for="(post, index) in searchedPosts" :key="index">
          <FeedItem :post="post" />
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

<script setup lang="ts">
import PeopleYouMayKnow from "@/components/PeopleYouMayKnow.vue";
import Trends from "@/components/Trends.vue";
import { ref } from "vue";
import FeedItem from "@/components/FeedItem.vue";
import { usePostStore } from "@/stores/posts";
import { storeToRefs } from "pinia";

const searchQuery = ref(null);

const searchedUsers = ref(null);

const searchedPosts = ref(null);

const postStore = usePostStore();

const { searchData } = storeToRefs(postStore);

const handleSearch = async () => {
  await postStore.searchPosts(searchQuery.value);
  searchedUsers.value = searchData.value.users;
  searchedPosts.value = searchData.value.posts;
};
</script>
