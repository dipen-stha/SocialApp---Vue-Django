<script setup lang="ts">
import BaseModal from '@/components/BaseModal.vue';
import { ref } from 'vue'

const modalActive = ref(null);

const toggleModal = () => {
    modalActive.value = !modalActive.value;
}
</script>

<template>
    <BaseModal :modalActive="modalActive">
    </BaseModal>
</template>