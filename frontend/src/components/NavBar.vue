<template>
  <nav class="py-10 px-8 border-b border-stone-200 dark:border-stone-700 primary-background">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">
        <div class="menu-left">
          <RouterLink to="#" class="text-xl text-stone-900 dark:text-stone-50">Chat</RouterLink>
        </div>
        <div v-if="isAuthenticated" class="menu-center flex space-x-12">
          <RouterLink to="/feed" class="text-sky-500">
            <div
              class=""
            >
              <Icon name="House" class="text-sky-500 dark:text-sky-600 color-transition hover:text-amber-300 hover:scale-110"/>
            </div>
          </RouterLink>
          <div>
            <Dropdown title="Chats" width="lg">
              <template #icon>
                <Icon name="MessageCircle" class="text-sky-500 dark:text-sky-600 color-transition hover:text-amber-300 hover:scale-110"/>
              </template>
              <template #body>
                <div v-if="chatList" class="flex flex-col">
                  <div v-for="chat in chatList">
                    <div
                      class="p-2 border-b border-stone-200 dark:border-stone-500 color-transition bg-stone-50 hover:bg-stone-300 dark:hover:bg-zinc-800"
                      :class="chat.is_read ? 'bg-stone-50 dark:bg-zinc-500' : 'bg-stone-200 dark:bg-zinc-600'"
                    >
                      <div class="flex gap-x-[10px] items-center">
                        <img :src="getUser(chat).avatar" class="avatar" />
                        <span>{{ chat.latest_message }}</span>
                        <span class="ml-auto text-sm dark:text-stone-50 text-stone-900">{{
                          timeAgo(chat.modified_at)
                        }}</span>
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
          <div @click="onNotificationOpen">
            <Dropdown width="lg">
              <template #icon>
                <Icon name="Bell" class="text-sky-500 dark:text-sky-600 color-transition hover:text-amber-300 hover:scale-110"/>
              </template>
              <template #body>
                <div v-if="notificationList" class="flex flex-col">
                  <div v-for="notification in notificationList">
                    <div class="flex gap-x-[10px] items-center p-2 border-b border-stone-200 dark:border-stone-500 color-transition bg-stone-50 dark:bg-zinc-700 hover:bg-stone-300 dark:hover:bg-zinc-800 w-full">
                      <img class="avatar" :src="notification.created_by.avatar"/>
                      <div class="flex justify-between text-stone-900 dark:text-stone-50 w-full">
                        <div class="">{{ notification.body }}</div>
                        <div class="text-sm">{{ timeAgo(notification.created_at) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
            </Dropdown>
          </div>

          <RouterLink to="/search">
            <Icon name="Search" class="text-sky-500 dark:text-sky-600 color-transition hover:text-amber-300 hover:scale-110"/>
          </RouterLink>
        </div>
        <template class="menu-right" v-if="userStore && isAuthenticated">
          <div id="profileDropdown" class="relative">
            <div @click.stop="toggleDropdown">
              <img
                :src="userStore.self.avatar"
                class="rounded-full h-10 w-10 transition delay-25 duration-300 ease-in-out hover:scale-125 cursor-pointer hover:shadow-md"
              />
            </div>

            <transition
              enter-active-class="transition-all duration-300 ease-out"
              enter-from-class="transform opacity-0 -translate-y-4 max-h-0"
              enter-to-class="transform opacity-100 translate-y-0 max-h-40"
              leave-active-class="transition-all duration-200 ease-in"
              leave-from-class="transform opacity-100 translate-y-0 max-h-40"
              leave-to-class="transform opacity-0 -translate-y-4 max-h-0"
            >
              <div
                v-if="showDropdown"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg overflow-hidden origin-top"
                @click.stop
              >
                <div class="">
                  <RouterLink
                    :to="{ name: 'profile', params: { id: userId } }"
                    class="block px-4 py-2 text-gray-800 hover:bg-gray-100 transition-colors duration-200"
                  >
                    Profile
                  </RouterLink>
                  <div
                    @click="logout"
                    class="block px-4 py-2 text-gray-800 hover:bg-gray-100 transition-colors duration-200 cursor-pointer"
                  >
                    Logout
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useUserStore } from "@/stores/user/user";
import { watch, computed, ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import Dropdown from "./Dropdown.vue";
import { storeToRefs } from "pinia";
import Icon from "./Icon.vue";
import { useChatStore } from "@/stores/chat";
import { useAuthStore } from "@/stores/user/auth";
import { useNotificationStore } from "@/stores/notification";
import { timeAgo } from "@/utils/timeAgo";

const userStore = useUserStore();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();
const chatStore = useChatStore();

const router = useRouter();
const { isAuthenticated } = storeToRefs(userStore);
const { chatList } = storeToRefs(chatStore);
const { notificationList, notificationStats } = storeToRefs(notificationStore);

const userId = computed(() => userStore.self.id);

const showDropdown = ref(false)
const trigger =ref(null)
const dropDown = ref(null)

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const logout = () => {
  authStore.userLogout();
  showDropdown.value = false
  router.push("/login");
}

const closeOnClickOutside = (event) => {
  if (
    showDropdown.value = false &&
    !trigger.value.contains(event.target) &&
    !dropDown.value.contains(event.target)
  ) {
    showDropdown.value = false
  }
}

const onNotificationOpen = async () => {
  await notificationStore.fetchNotificationList();
}

onMounted(() => {
  document.addEventListener('click', closeOnClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', closeOnClickOutside)
})

const getNotifications = () => {
  notificationStore.fetchNotificationList();
};

const getUser = (chatObject) => {
  return chatObject.users.find((item) => item.id !== userStore.self.id)
};

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
  notificationStore.fetchNotificationStats();
  getChats();
});
</script>
