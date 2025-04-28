<template>
  <div class="p-4 bg-white border border-gray-200 mb-6 rounded">
    <div class="flex justify-between mb-6 items-center">
      <div class="flex items-center space-x-4">
        <img :src="post.created_by.avatar" class="rounded-full h-10 w-10" />
        <p>
          <strong>{{ post.created_by.name }}</strong>
        </p>
      </div>
      <div class="text-gray-400 text-xs">
        {{ post.created_at_formatted }} ago
      </div>
    </div>
    <div v-if="post.attachments[0]">
      <img :src="post.attachments[0].image" class="rounded-lg w-full" />
      <p>{{ post.body }}</p>
    </div>
    <div v-else class="py-2">
      <p>{{ post.body }}</p>
      <p class="text-gray-500 text-xs">#asdas #asdasd</p>
    </div>
    <div class="my-6 flex justify-between">
      <div class="flex space-x-6">
        <div class="flex items-center space-x-2">
          <button
            @click="handleLike(post.id)"
            class="cursor-pointer transition delay-25 duration-300 ease-in-out hover:scale-125"
          >
            <Icon name="Heart" />
          </button>
          <span class="text-gray-500 text-xs"
            >{{ post.likes_count }} likes</span
          >
        </div>
        <div class="flex items-center space-x-2">
          <button
            @click="onComment(post.id)"
            class="cursor-pointer transition delay-25 duration-300 ease-in-out hover:scale-125"
          >
            <Icon name="MessageSquareMore" />
          </button>
          <span class="text-gray-500 text-xs"
            >{{ post.comments_count }} comments</span
          >
        </div>
      </div>
      <div class="cursor-pointer transition delay-25 duration-300 ease-in-out hover:scale-125">
        <Icon name="EllipsisVertical" />
      </div>
    </div>
  </div>
  <!-- <BaseModal :modalActive="modalActive" @close-modal="toggleModal(post.id)">
    <PostDetail v-if="postDetail" :postDetail="postDetail" />
  </BaseModal> -->
  <BaseModal
      v-model:show="showModal"
      title="Custom Modal Title"
      :width="600"
      :height="400"
      :actions="[
        { title: 'Close', emit: 'close' },
        { title: 'Save', emit: 'save' }
      ]"
      @action="handleModalAction"
    >
      <div class="space-y-4">
        <h3 class="text-lg font-medium">Modal Content</h3>
        <p>This is the dynamic content area. You can put anything here.</p>
        <input 
          v-model="inputValue"
          class="w-full p-2 border rounded-md"
          placeholder="Type something..."
        />
      </div>
    </BaseModal>
</template>

<script setup>
import axios from "axios";
import { onMounted, onUnmounted, ref, watch } from "vue";
import BaseModal from "./BaseModal.vue";
import PostDetail from "./PostDetail.vue";
import { toggleBodyScroll } from "@/utils/scroll";
import Icon from "./Icon.vue";
import { usePostStore } from "@/stores/posts";

const props = defineProps({
  post: Object || null,
});

const postStore = usePostStore();

const postDetail = ref(null);
const showModal = ref(false);

const handleLike = async (postId) => {
  await postStore.createLikes(postId);
};

const onComment = () => {
  showModal.value = true
}

</script>

<style scoped>
body {
  scrollbar-gutter: stable;
}
</style>
