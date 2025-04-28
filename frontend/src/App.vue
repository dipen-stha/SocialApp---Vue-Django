<template>
  <div class="fixed inset-0 bg-stone-50 dark:bg-stone-900 -z-10"></div>
  <div class="relative text-stone-900 dark:text-stone-50">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
</script>