<template>
  <div class="fixed inset-0 -z-10"></div>
  <div class="relative primary-text">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView, useRoute } from "vue-router";

const route = useRoute();
</script>