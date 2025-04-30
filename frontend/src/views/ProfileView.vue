<template>
  <div v-if="user" class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div
        class="p-4 primary-background primary-border rounded-lg text-center"
      >
        <img :src="user.avatar" class="rounded-full m-auto w-15 h-15" />
        <p class="mt-4 text-xl font-semibold">{{ user.name }}</p>
        <p>{{ user.email }}</p>
        <div class="mt-6 flex space-x-8 justify-around">
          <RouterLink :to="{ name: 'friends', params: { id: user.id } }">
            <p class="text-xs primary-text">
              {{ userStats?.friends_count }} friends
            </p>
          </RouterLink>
          <p class="text-xs primary-text">
            {{ userStats?.posts_count }} posts
          </p>
        </div>
        <div v-if="self?.id !== route.params.id" class="">
          <div
            v-if="relationshipState === 'friends'"
            class="flex flex-wrap gap-y-2"
          >
            <button
              class="btn-primary mt-4 text-white w-1/2"
            >
              <span class="flex space-x-2 text-xs color-transition">
                <Icon name="Users" :stroke-width="2" :size="16"/>
                <p>Friends</p>
              </span>
            </button>
            <button
              class="bg-red-500 hover:bg-red-600 px-2 py-2 rounded-md mt-4 text-white w-1/2 color-transition"
            >
              <span class="flex space-x-2 text-xs">
                <Icon name="UserRoundMinus" :stroke-width="2" :size="16"/>
                <p>Unfriend</p>
              </span>
            </button>
            <button
              class="py-1 px-2 bg-blue-500 hover:bg-blue-700 w-full rounded-lg color-transition"
            >
              <span class="text-white"> Message </span>
            </button>
          </div>

          <div v-else-if="relationshipState === 'request_sent'" class="">
            <button
              @click=""
              class="bg-gray-500 hover:bg-gray-700 px-3 py-2 rounded-lg mt-4 w-full text-white"
            >
              <span class="flex space-x-4">
                <Icon name="UserRoundCheck" class=""/>
                <p>Request Sent</p>
              </span>
            </button>
          </div>
          <div v-else-if="relationshipState === 'not_friends'" class="flex mt-3 items-center lg:px-[30px] md:px-[5px]">
            <button
              @click="sendRequest"
              class="btn-primary w-full"
            >
              <div class="flex justify-center items-center space-x-[10px]">
                <Icon name="UserPlus" />
                  <p class="text-center hidden md:block">Add Friend</p>
              </div>
            </button>
          </div>
          <div
            v-else-if="!isFriend && hasRequest"
            class="flex space-x-2 justify-center text-center"
          >
            <button
              class="bg-sky-500 hover:bg-sky-600 px-2 py-2 rounded-lg mt-4 text-white w-1/2 transition duration-200 ease-in"
              @click="handleRequest('accepted')"
            >
              <span class="flex justify-center items-center space-x-2 text-xs">
                <Icon name="Check" :stroke-width="2" :size="16"/>
                <p class="hidden md:block">Accept</p>
              </span>
            </button>
            <button
              class="bg-red-500 hover:bg-red-600 px-2 py-2 rounded-lg mt-4 text-white w-1/2 text-center transition duration-200 ease-in"
              @click="handleRequest('rejected')"
            >
              <span class="flex justify-center items-center space-x-2 text-xs text-center">
                <Icon name="Ban" class="text-xs" :stroke-width="2" :size="16"/>
                <p class="hidden md:block">Reject</p>
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="main-middle col-span-2 space-y-4">
      <div
        v-if="userStore.user.id === self.id"
        class="p-4 border border-stone-200 dark:border-stone-700 rounded"
      >
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
      <div v-for="(post, index) in postList" :key="index">
        <FeedItem :post="post" />
      </div>
    </div>
    <div class="main-right col-span-1">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>

<script setup lang="ts">
import FeedItem from "@/components/FeedItem.vue";
import Icon from "@/components/Icon.vue";
import PeopleYouMayKnow from "@/components/PeopleYouMayKnow.vue";
import Trends from "@/components/Trends.vue";
import { useFriendStore } from "@/stores/friends";
import { usePostStore } from "@/stores/posts";
import { useUserStore } from "@/stores/user/user";
import axios from "axios";
import { storeToRefs } from "pinia";
import { onMounted, ref, reactive, watch, onUnmounted } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";

const userStore = useUserStore();
const postStore = usePostStore();
const friendStore = useFriendStore();

onMounted(() => {
  if (route.params.id) {
    userStore.fetchUserDetail(route.params.id);
    userStore.fetchUserStats(route.params.id);
    postStore.fetchPostList(route.params.id);
    friendStore.fetchFriends(self.value.id);
    friendStore.fetchFriendRequest();
    determineRelationshipState();
  }
});

const posts = ref([]);

const route = useRoute();

const { self, user, userStats } = storeToRefs(userStore);
const { postList } = storeToRefs(postStore);
const { friendsList, friendsRequestsList } = storeToRefs(friendStore);

const content = reactive({
  body: "",
  attachments: [],
});

const friendRequest = ref(null);

const isFriend = ref(false);

const hasRequest = ref(false);

const relationshipState = ref("");

const handleSubmit = async () => {
  await axios.post("/api/posts/", content).then((response) => {
    posts.value.unshift(response.data);
    content.body = "";
  });
};

const determineRelationshipState = () => {
  if(!friendsRequestsList.value || friendsRequestsList.value.length === 0) return;
  try {
    const currentUserId = self.value.id;
    const sentRequest = friendsRequestsList.value.find(
      (item) =>
        item.created_for.id === route.params.id &&
        item.created_by.id === currentUserId
    );
    const receivedRequest = friendsRequestsList.value.find(
      (item) =>
        item.created_by.id === route.params.id &&
        item.created_for.id === currentUserId
    );
    if (friendsRequestsList.value.find(
      (item) => 
      item.created_for.id === currentUserId ||
      item.created_by.id === currentUserId &&
      item.status === 'accepted')) {
      relationshipState.value = "friends";
      isFriend.value = true;
    } else if (sentRequest) {
      relationshipState.value = "request_sent";
      friendRequest.value = sentRequest;
    } else if (receivedRequest) {
      relationshipState.value = "request_received";
      friendRequest.value = receivedRequest;
      hasRequest.value = true;
    } else {
      relationshipState.value = "not_friends";
    }
  } catch (error) {
    console.log(error);
  }
};

const sendRequest = async () => {
  friendStore.sendFriendRequest(route.params.id);
};

const handleRequest = async (status: string) => {
  try {
    friendStore.udpateFriendRequest(friendRequest.value.id, status);
    if (status === "accepted") {
      relationshipState.value = "friends";
      isFriend.value = true;
    } else {
      relationshipState.value = "not_friends";
      hasRequest.value = false;
    }
    friendRequest.value = null;
  } catch (error) {
    console.error(error);
  }
};

watch(
  () => route.params,
  () => {
    determineRelationshipState();
  }
);

watch(
  () => friendsRequestsList.value,
  (newVal) => {
    if(newVal && newVal.length > 0){
      determineRelationshipState();
    }
  }
)

onBeforeRouteLeave(() => {
  userStore.$reset();
  postStore.$reset();
  friendStore.$reset();
})
</script>
