
<template>
  <NavBar :isAuthenticated="userStore.user.isAuthenticated" :userId="userStore.user.id" />
  <main class="px-8 py-6 bg-gray-100">
    <RouterView />
  </main>
  <Toast />
</template>

<style scoped>

</style>

<script setup>
import axios from 'axios'
import NavBar from './components/NavBar.vue';
import Toast from './components/Toast.vue';
import { useUserStore } from './stores/user';
import { onBeforeMount } from 'vue';

const userStore = useUserStore()

onBeforeMount(() => {
  userStore.initStore();
  const token = userStore.user.access
  if(token) {
    axios.defaults.headers.common["Authorization"] = "Bearer " + token;
  } else {
    axios.defaults.headers.common["Authorization"] = ''
  }
}) 
</script>