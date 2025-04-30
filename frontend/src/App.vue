<template>
  <div class="fixed inset-0 primary-background -z-10"></div>
  <div class="relative primary-text">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
</script>