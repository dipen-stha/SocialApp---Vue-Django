<script setup>

defineEmits(["close-modal"]);
defineProps({
    modalActive: {
        type: Boolean,
        default: false
    }
})
</script>

<template>
    <Teleport to="body">
    <Transition name="modal-outer">
        <div v-show="modalActive"
            class="fixed w-full bg-black bg-opacity-30 h-screen top-0 left-0 flex justify-center px-8 overflow-auto">
            <Transition name="modal-inner">
                <div v-if="modalActive" class="p-4 bg-gray-100 self-start mt-32 w-full max-w-screen-md rounded-md">
                    <div class="flex justify-end">
                            <button class="text-white bg-red-500 px-2 py-1 rounded-lg hover:bg-red-700" @click="$emit('close-modal')">
                                Close
                            </button>
                    </div>
                    <slot />
                </div>
            </Transition>
        </div>
    </Transition> 
</Teleport>
</template>

<style scoped>
/* Outer container transitions (backdrop) */
.modal-outer-enter-active,
.modal-outer-leave-active {
  transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1); /* Smooth easing */
}

.modal-outer-enter-from,
.modal-outer-leave-to {
  opacity: 0;
}

/* Inner content transitions (modal) */
.modal-inner-enter-active {
  transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.4, 0, 0.2, 1) 0.1s; /* Slight delay for scaling */
}

.modal-inner-leave-active {
  transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-inner-enter-from {
  opacity: 0;
  transform: scale(0.9); /* Slightly larger scale to make it smoother */
}

.modal-inner-leave-to {
  opacity: 0;
  transform: scale(0.95); /* Slightly smaller scale for a polished zoom-out effect */
}

</style>