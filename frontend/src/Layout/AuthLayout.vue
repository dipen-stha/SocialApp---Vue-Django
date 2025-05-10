<script setup lang="ts">
import NavBar from '@/components/NavBar.vue';

</script>

<template>
    <div class="primary-background ">
        <NavBar></NavBar>
    <div class="pt-[65px]! pb-10! p-4 h-screen">
        <RouterView />
    </div>
    </div>
</template>