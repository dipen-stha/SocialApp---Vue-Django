<template>
  <div class="relative">
    <!-- Dropdown trigger button -->
    <button
      id="dropdownNotificationButton"
      ref="trigger"
      @click="toggleDropdown"
      class="relative inline-flex items-center text-sm font-medium text-center"
      type="button"
    >
      <slot name="icon">
      </slot>

      <div
        v-if="showBadge"
        class="absolute block w-3 h-3 bg-red-500 border-stone-200 dark:border-stone-700 rounded-full -top-0.5 start-2.5"
      ></div>
    </button>

    <!-- Updated transition for top-to-bottom animation -->
    <transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="transform opacity-0 -translate-y-2"
      enter-to-class="transform opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="transform opacity-100 translate-y-0"
      leave-to-class="transform opacity-0 -translate-y-2"
    >    
      <div
        v-show="isOpen"
        ref="dropdown"
        id="dropdownNotification"
        class="absolute z-20 mt-2 left-1/2 transform -translate-x-1/2 w-full bg-stone-50 dark:bg-stone-900 divide-y divide-gray-100 rounded-lg shadow-md border border-stone-200 dark:border-stone-700"
        :class="dropdownClasses"
        :style="{ width: widthClass }"
      >
        <div
          class="block px-4 py-2 text-center text-gray-100 rounded-t-lg bg-sky-500 dark:bg-stone-800"
        >
          <slot name="title">{{ title }}</slot>
        </div>

        <div class="divide-y divide-gray-100 dark:divide-gray-700 max-h-96 overflow-y-auto">
          <slot name="body">
            <div class="px-4 py-3 text-center text-gray-500 dark:text-gray-400">
              No notifications
            </div>
          </slot>
        </div>

        <slot name="footer">
          <a
            href="#"
            class="block py-2 text-sm font-medium text-center text-stone-900 dark:text-stone-50 rounded-b-lg bg-stone-100 dark:bg-stone-700 color-transition hover:bg-stone-200 hover:dark:bg-stone-800"
          >
            <div class="inline-flex items-center">
              <Icon name="Eye"/>
              View all
            </div>
          </a>
        </slot>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import Icon from './Icon.vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Notifications'
  },
  showBadge: {
    type: Boolean,
    default: false
  },
  dropdownClasses: {
    type: String,
    default: ''
  },
  position: {
    type: String,
    default: 'right',
    validator: (value) => ['right', 'left'].includes(value)
  },
  width: {
    type: String,
    default: 'sm',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl', 'full', 'auto'].includes(value) || value.match(/^\d+(px|rem|em|%)?$/)
  }
})

const widthClass = computed(() => {
  if (props.width.match(/^\d/)) {
    return ''
  }
  const widthMap = {
    xs: '320px',  // 20rem (320px)
    sm: '384px',  // 24rem (384px)
    md: '448px',  // 28rem (448px)
    lg: '512px',  // 32rem (512px)
    xl: '576px',  // 36rem (576px)
    full: '100%',
    auto: 'auto'
  }
  
  return widthMap[props.width] || 'max-w-lg'
})

const isOpen = ref(false)
const trigger = ref(null)
const dropdown = ref(null)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const handleClickOutside = (event) => {
  if (
    isOpen.value &&
    !trigger.value.contains(event.target) &&
    !dropdown.value.contains(event.target)
  ) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>