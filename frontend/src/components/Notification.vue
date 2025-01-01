<template>
  <div class="absolute z-20 w-full max-w-sm bg-white divide-y divide-gray-100 rounded-lg shadow">
    <div class="block px-4 py-2 font-medium text-center text-gray-700 rounded-t-lg bg-gray-50">
      {{ title }}
    </div>
    <div v-for="item in items" class="divide-y divide-gray-100 hover:bg-gray-100" :class="!item.is_read? 'bg-purple-50' : ''">
      <a href="#" class="flex px-4 py-3">
        <div class="flex space-x-4 flex-shrink-0 items-center ">
          <img src="" class="h-10 w-10 rounded-full" />
          <div>
            <p>{{item.body}}</p>
          </div>
        </div>
      </a>
    </div>
    <a href="#">
    <div class="px-4 py-3 hover:bg-gray-200 hover:font-semibold hover:rounded-b">
        <div class="flex justify-center items-center">
          View all
        </div>
      </div>
    </a>
  </div>
</template>

<script setup>

const props = defineProps({
  title: String,
  items: Object,
  isMessage: Boolean

});
</script>

<style scoped>
</style>