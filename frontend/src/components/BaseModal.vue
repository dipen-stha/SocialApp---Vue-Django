<template>
  <Transition name="modal">
    <div 
      v-if="show" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50"
      @click.self="closeModal"
    >
      <div 
        class="bg-white rounded-md shadow-xl overflow-hidden"
        :style="{
          width: typeof width === 'number' ? `${width}px` : width,
          // height: typeof height === 'number' ? `${height}px` : height,
          maxWidth: '90vw',
          maxHeight: '90vh'
        }"
      >
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b">
          <h2 class="text-lg font-semibold">{{ title }}</h2>
          <button 
            @click="closeModal"
            class="p-1 rounded-full hover:bg-gray-100"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Content -->
        <div class="p-4 overflow-y-auto" :style="{ height: 'calc(100% - 112px)' }">
          <slot></slot>
        </div>
        
        <!-- Footer -->
        <div class="flex justify-end items-center p-4 border-t gap-2 w-full">
          <button
            v-for="(action, index) in actions"
            :key="index"
            @click="handleAction(action.emit)"
            class="px-4 py-2 text-sm font-medium rounded-md"
            :class="[
              index === 0 ? 'btn-secondary' : 'btn-primary',
              actions.length > 1 && index === 0 ? 'mr-2' : ''
            ]"
          >
            {{ action.title }}
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: 'Modal Title'
  },
  width: {
    type: [String, Number],
    default: '500px'
  },
  height: {
    type: [String, Number],
    default: 'auto'
  },
  actions: {
    type: Array,
    default: () => [
      { title: 'Cancel', emit: 'cancel' },
      { title: 'Confirm', emit: 'confirm' }
    ],
    validator: (value) => value.length <= 2
  }
});

const emit = defineEmits(['update:show', 'action']);

const closeModal = () => {
  emit('update:show', false);
};

const handleAction = (actionName) => {
  emit('action', actionName);
  if (actionName === 'cancel') {
    closeModal();
  }
};
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}
</style>