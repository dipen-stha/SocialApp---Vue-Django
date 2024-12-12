<script setup>
import { useUserStore } from '@/stores/user';
import { watch, computed, onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';

const userStore = useUserStore()

const router = useRouter();
const isAuthenticated = computed(() =>userStore.user.isAuthenticated)
const userId = computed(() => userStore.user.id)

onBeforeMount(() => {
  
})

const logout = () => {
  userStore.removeToken()
  router.push('/login')
}

watch(userStore, () => {

})
</script>

<template>
  <nav class="py-10 px-8 border-b border-gray-200">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">
        <div class="menu-left">
          <RouterLink to="#" class="text-xl">Chat</RouterLink>
        </div>

        <div v-if="isAuthenticated" class="menu-center flex space-x-12">
          <RouterLink to="/feed" class="text-purple-700 hover:text-purple-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
          </RouterLink>
          <RouterLink to="/chat" class="hover:text-purple-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
            </svg>
          </RouterLink>
          <RouterLink to="#" class="hover:text-purple-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
            </svg>
          </RouterLink>
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