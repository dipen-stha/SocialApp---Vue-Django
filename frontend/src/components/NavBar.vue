<template>
  <nav class="py-10 px-8 border-b border-gray-200">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">
        <div class="menu-left">
          <RouterLink to="#" class="text-xl">Chat</RouterLink>
        </div>
        <div v-if="isAuthenticated" class="menu-center flex space-x-12">
          <RouterLink to="/feed" class="text-purple-700 hover:text-purple-500">
            <div class="transition delay-10 duration-300 ease-in-out hover:scale-110">
              <Icon name="House" />
            </div>
          </RouterLink>
          <div>
            <Dropdown title="Chats" width="lg">
              <template #icon>
                <Icon name="MessageCircle"/>
              </template>
              <template #body>
                <div v-if="chatList" class="flex flex-col">
                  <div v-for="chat in chatList">
                    <div class="p-2 border-b color-transition hover:bg-gray-100" :class="chat.is_read ? '' : 'bg-gray-50'">
                      <div class="flex gap-x-[5px] items-center">
                        <img :src="getUser(chat).avatar" class="avatar"/>
                        <span>{{ chat.message }}</span>
                        <span class="ml-auto text-sm text-gray-600">{{ chat.formatted_created_at }}</span>
                    </div>
                    </div>
                  </div>
                </div>
                <div v-else>
                  <span clsas="text-lg font-semibold">No Notifications</span>
                </div>
              </template>
            </Dropdown>
          </div>
          <div>
            <Dropdown width="lg">
              <template #icon>
                <Icon name="Bell" />
              </template>
              <template #body>
                <ul>
                  <li v-for="notification in notificationList">
                    <div class="flex gap-x-[5px] items-center">
                      <img class="avatar"/>
                    </div>
                  </li>
                </ul>
              </template>
            </Dropdown>
          </div>
          

          <RouterLink to="/search" class="hover:text-purple-500">
            <Icon name="Search"/>
          </RouterLink>
        </div>
        <template class="menu-right" v-if="userStore && isAuthenticated">
          <div class="group relative">
            <div>
              <img
                :src="userStore.user.avatar"
                class="rounded-full h-10 w-10"
              />
            </div>
            <div
              class="hidden group-hover:block absolute right-3 bg-gray-200 rounded-l-lg rounded-br-lg"
            >
              <div
                v-if="userId"
                class="hover:bg-gray-500 text-gray-800 hover:text-white w-full rounded-tl-lg px-3 py-2 cursor-pointer"
              >
                <RouterLink :to="{ name: 'profile', params: { id: userId } }"
                  >Profile
                </RouterLink>
              </div>
              <div
                class="hover:bg-gray-500 text-gray-800 hover:text-white w-full rounded-b-lg px-3 py-2 cursor-pointer"
                @click="logout"
              >
                Logout
              </div>
            </div>
          </div>
        </template>
        <template v-else class="menu-right">
          <div class="">
            <RouterLink to="/login">
              <button
                class="px-3 py-2 bg-purple-500 hover:bg-purple-700 mx-2 rounded-lg text-white"
              >
                Login
              </button>
            </RouterLink>
            <RouterLink to="/signup">
              <button
                class="px-3 py-2 bg-purple-500 hover:bg-purple-700 mx-2 rounded-lg text-white"
              >
                Sign Up
              </button>
            </RouterLink>
          </div>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useUserStore } from "@/stores/user/user";
import axios from "axios";
import { watch, computed, ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import Dropdown from "./Dropdown.vue";
import { storeToRefs } from "pinia";
import Icon from "./Icon.vue";
import { useChatStore } from "@/stores/chat";
import { useAuthStore } from "@/stores/user/auth";
import { useNotificationStore } from "@/stores/notification";

const userStore = useUserStore();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();
const chatStore = useChatStore();

const router = useRouter();
const { isAuthenticated } = storeToRefs(userStore);
const { chatList } = storeToRefs(chatStore);
const { notificationList, notificationStats } = storeToRefs(notificationStore)

const userId = computed(() => userStore.user.id);

const logout = () => {
  
};

const getNotifications = () => {
  notificationStore.fetchNotificationList();
}

const getUser = (chatObject) => {
  if(chatObject.created_by.id === userStore.user.id) return chatObject.sent_to
  return chatObject.created_by
}

const getChats = async () => {
  await chatStore.fetchChatList();
};

const notification = ref(null);
let socket = null;
let socketUrl = "ws://localhost:8000/ws/notify/";

const connectSocket = async () => {
  socket = new WebSocket(socketUrl);

  socket.onopen = () => {
    console.log("Socket Connected");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    notification.value = data.message;
    getNotificationCount();
    getNotifications();
  };

  socket.onclose = () => {
    console.log("WebSocket connection closed");
  };
};

onBeforeUnmount(() => {
  if (socket) {
    socket.close();
  }
});

onMounted(() => {
  connectSocket();
  notificationStore.fetchNotificationStats()
  getChats();
});
</script>
