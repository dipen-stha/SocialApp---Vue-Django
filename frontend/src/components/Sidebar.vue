<template>
  <div
    :class="[
      'h-screen transition-all duration-500 z-30 shadow-md admin-border overflow-hidden admin-text',
      show ? 'w-64' : 'w-12',
    ]"
  >
    <div v-if="show" class="flex justify-between items-center px-4 py-4">
      <span class="text-2xl font-bold truncate">Sidebar</span>
      <button @click="$emit('toggle')">
        <Icon name="PanelRightOpen" :size="32" class="color-transition hover:text-sky-300 hover:scale-110 text-gray-500" />
      </button>
    </div>

    <div v-if="show" class="flex-1 overflow-y-auto overflow-x-hidden py-6">
      <div v-for="(item, i) in SideBarItems" :key="i" class="mb-2 ">
        <div v-if="isParent(item)" class="flex flex-col">
          <div class="border-b py-2 border-gray-300">
            <span class="ml-[20px]">{{ item.label }}</span>
          </div>
          <div v-for="childItem in item.child">
            <RouterLink :to="childItem.to">
              <div class="flex gap-x-[15px] py-2 ml-[20px]">
                <Icon :name="childItem.icon" />
                <span class="truncate">{{ childItem.label }}</span>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

    <button
      v-show="!show"
      @click="$emit('toggle')"
      class="h-10 w-10 mt-3 ml-1 flex items-center text-gray-500 justify-center"
    >
      <Icon
        name="PanelLeftOpen"
        :size="32"
        class="color-transition hover:text-sky-300 hover:scale-110"
      />
    </button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import Icon from './Icon.vue'
import { SideBarItems } from '@/utils/setup/sideBarItems'

const props = defineProps({
  show: Boolean
})
const emit = defineEmits(['toggle'])

const isParent = (item) => item.child?.length > 0
</script>

