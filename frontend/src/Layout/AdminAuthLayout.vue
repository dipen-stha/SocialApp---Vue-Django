<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'

const showSidebar = ref(true)

const toggleSidebar = () => {
  showSidebar.value = !showSidebar.value
}
</script>

<template>
  <div class="flex h-screen admin-background">
    <Sidebar :show="showSidebar" @toggle="toggleSidebar" />

    <div
      class="transition-all duration-500 w-full"
    >
      <RouterView />
    </div>
  </div>
</template>
