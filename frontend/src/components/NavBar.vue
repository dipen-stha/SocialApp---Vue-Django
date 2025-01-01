<template>
  <nav class="py-10 px-8 border-b border-gray-200">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">
        <div class="menu-left">
          <RouterLink to="#" class="text-xl">Chat</RouterLink>
        </div>

        <div v-if="isAuthenticated" class="menu-center flex space-x-12">
          <RouterLink to="/feed" class="text-purple-700 hover:text-purple-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
          </RouterLink>
          <div class="">
            <div class="relative w-fit">
            <div
              class="absolute bottom-auto left-auto right-0 top-0 z-10 inline-block -translate-y-1/2 translate-x-2/4 rotate-0 skew-x-0 skew-y-0 scale-x-100 scale-y-100 whitespace-nowrap rounded-full bg-purple-700 px-2.5 py-1 text-center align-baseline text-xs font-bold leading-none text-white">
              2
            </div>
              <button class="relative z-10" @click="toggleDropdown('chat')">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
              </svg>
            </button>
          </div>
            <Notification v-if="chatIsOpen" :title="'Chat'" />
          </div>
          <div>
            <div class="relative w-fit">
            <div
              class="absolute bottom-auto left-auto right-0 top-0 z-10 inline-block -translate-y-1/2 translate-x-2/4 rotate-0 skew-x-0 skew-y-0 scale-x-100 scale-y-100 whitespace-nowrap rounded-full bg-purple-700 px-2.5 py-1 text-center align-baseline text-xs font-bold leading-none text-white">
              {{unreadNotification}}
            </div>
            <button class="relative z-10" @click="toggleDropdown('notification')">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
              </svg>
            </button>
          </div>
            <Notification v-if="notificationIsOpen" :title="'Notification'" :items="notifications"/>
          </div>

          <RouterLink to="/search" class="hover:text-purple-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
          </RouterLink>
        </div>
        <template class="menu-right" v-if="userStore && isAuthenticated">
            <div class="group relative">
              <div>
                <img :src="userStore.user.avatar"
                  class="rounded-full h-10 w-10" />
              </div>
              <div class="hidden group-hover:block absolute right-3 bg-gray-200 rounded-l-lg rounded-br-lg">
                <div v-if="userId" class="hover:bg-gray-500 text-gray-800 hover:text-white w-full rounded-tl-lg px-3 py-2 cursor-pointer">
                  <RouterLink :to="{name:'profile', params:{ id:userId }}">Profile
                  </RouterLink>
                </div>
                <div class="hover:bg-gray-500 text-gray-800 hover:text-white w-full rounded-b-lg px-3 py-2 cursor-pointer" @click="logout">Logout</div>
              </div>
            </div>
        </template>
        <template v-else class="menu-right">
          <div class="">
            <RouterLink to="/login">
              <button class="px-3 py-2 bg-purple-500 hover:bg-purple-700 mx-2 rounded-lg text-white">Login</button>
            </RouterLink>
            <RouterLink to="/signup">
              <button class="px-3 py-2 bg-purple-500 hover:bg-purple-700 mx-2 rounded-lg text-white">Sign Up</button>
            </RouterLink>
          </div>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { watch, computed, ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import Notification from './Notification.vue';

const userStore = useUserStore()

const router = useRouter();
const isAuthenticated = computed(() => userStore.user.isAuthenticated)
const userId = computed(() => userStore.user.id)
const unreadNotification = ref(null);
const notifications = ref(null);

const notificationIsOpen = ref(false)
const chatIsOpen = ref(false)

const toggleDropdown = (type) => {
  if(type === 'notification') {
    notificationIsOpen.value = !notificationIsOpen.value
    chatIsOpen.value = false
  } else {
    chatIsOpen.value = !chatIsOpen.value
    notificationIsOpen.value = false
  }
}

const logout = () => {
  userStore.removeToken()
  router.push('/login')
}

const getNotificationCount = async () => {
  try{
    const response = await axios.get('/api/notification/get_count/')
    if(response.data){
      unreadNotification.value = response.data.data.unread_notifications
  }
  } catch(error) {
    console.log(error)
  }
}

const getNotifications = async() => {
  try{
    const response = await axios.get('api/notification/list_notifications/')
    if(response.data){
      notifications.value = response.data
    }
  } catch(error){
    console.log(error)
  }
}

const notification = ref(null);
let socket = null;
let socketUrl = 'ws://localhost:8000/ws/notify/'

const connectSocket = async () => {
  socket = new WebSocket(socketUrl)

  socket.onopen = () => {
    console.log('Socket Connected');
  }

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    notification.value = data.message;
    getNotificationCount();
    getNotifications();
  };

  socket.onclose = () => {
    console.log('WebSocket connection closed')
  }
}

onBeforeUnmount(() => {
  if (socket) {
    socket.close();
  }
});

onMounted(() => {
  connectSocket();
  getNotificationCount();
  getNotifications();
})

</script>
