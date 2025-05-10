<template>
  <div class="flex flex-col h-screen w-full admin-text">
    <header class="h-16 admin-border p-4">
      <div class="flex items-center">
        <div class="ml-auto" v-if="userStore && isAuthenticated">
          <div id="profileDropdown" class="relative">
            <div @click.stop="toggleDropdown">
              <img
                :src="userStore.self.avatar"
                class="rounded-full h-10 w-10 transition delay-25 duration-300 ease-in-out hover:scale-125 cursor-pointer hover:shadow-md"
              />
            </div>

            <transition
              enter-active-class="transition-all duration-300 ease-out"
              enter-from-class="transform opacity-0 -translate-y-4 max-h-0"
              enter-to-class="transform opacity-100 translate-y-0 max-h-40"
              leave-active-class="transition-all duration-200 ease-in"
              leave-from-class="transform opacity-100 translate-y-0 max-h-40"
              leave-to-class="transform opacity-0 -translate-y-4 max-h-0"
            >
              <div
                v-if="showDropdown"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg overflow-hidden origin-top"
                @click.stop
              >
                <div class="">
                  <RouterLink
                    :to="{ name: 'profile', params: { id: self.id } }"
                    class="block px-4 py-2 text-gray-800 hover:bg-gray-100 transition-colors duration-200"
                  >
                    Profile
                  </RouterLink>
                  <div
                    @click="logout"
                    class="block px-4 py-2 text-gray-800 hover:bg-gray-100 transition-colors duration-200 cursor-pointer"
                  >
                    Logout
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </header>
    <main class="flex-1 overflow-auto p-4">
      <div class="">
        <div class="flex flex-col gap-y-[5px]">
            <div class="p-4 bg-gray-100 rounded-md">
                <div class="flex justify-between items-center">
                    <span class="text-3xl font-semibold">{{ props.title }}</span>
                    <div class="flex gap-x-[5px]">
                        <button v-for="(action, index) in props.actions" :key="index" class="btn-primary" @click="emit(action.emit)">{{ action.title }}</button>
                    </div>
                </div>
            </div>
            <div class="bg-gray-100 grow rounded-md">
                <slot name="body"></slot>
            </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useUserStore } from "@/stores/user/user";
import { storeToRefs } from "pinia";
import { ref, onMounted, onBeforeUnmount } from "vue";

const userStore = useUserStore();
const { isAuthenticated, self } = storeToRefs(userStore);

const showDropdown = ref(false);
const trigger = ref(null);
const dropDown = ref(null);

const props = defineProps({
    title: {
        type: Boolean,
        default: 'Layout'
    },
    actions: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits((event, ...args) => true)

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const logout = () => {
  authStore.userLogout();
  showDropdown.value = false;
  router.push("/login");
};

const closeOnClickOutside = (event) => {
  if (
    (showDropdown.value =
      false &&
      !trigger.value.contains(event.target) &&
      !dropDown.value.contains(event.target))
  ) {
    showDropdown.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", closeOnClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", closeOnClickOutside);
});

onMounted(() => {
  userStore.fetchSelfDetail();
});
</script>
