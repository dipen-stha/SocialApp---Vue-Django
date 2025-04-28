<template>
  <div class="bg-zinc-200 dark:bg-zinc-800 h-screen">
    <div class="h-screen flex justify-center items-center">
      <div class="min-h-[500px] min-w-[400px] bg-white dark:bg-zinc-500 rounded-md shadow-lg">
        <div class="text-center mt-[30px]">
          <span class="text-xl font-semibold">Login</span>
        </div>
        <form class="mt-[15px]" @submit.prevent="onLogin">
          <div class="flex h-full justify-center items-center">
            <div class="flex flex-col gap-y-[15px] w-[90%]">
              <div
                class="flex flex-col gap-y-[10px] border border-zinc-100 dark:border-zinc-700 p-4 rounded-md"
              >
                <div class="text-center" v-if="loginError">
                  <span class="text-red-500"
                    >Entered credentials do not match.</span
                  >
                </div>
                <div class="flex justify-center">
                  <input
                    type="text"
                    class="input-field w-full text-zinc-900"
                    placeholder="Enter Email"
                    v-model="loginPayload.email"
                  />
                </div>
                <div class="flex justify-center">
                  <input
                    type="password"
                    class="input-field w-full text-zinc-900"
                    placeholder="Enter Password"
                    v-model="loginPayload.password"
                  />
                </div>
              </div>
              <div>
                <button
                  type="submit"
                  class="w-full btn-primary"
                >
                  Login
                </button>
              </div>
              <div class="w-full text-center">
                <span
                  >Forgot your password?
                  <a href="#" class="text-blue-500">Click Here</a></span
                >
              </div>
              <div class="w-full text-center">
                <span
                  >New here? Sign up
                  <RouterLink to="/signup" class="text-blue-500">here</RouterLink></span
                >
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from "@/stores/user/user";
import { useAuthStore } from "@/stores/user/auth";
import { ref } from "vue";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const userStore = useUserStore();

const { loginPayload, loginError } = storeToRefs(authStore);

const onLogin = async () => {
  await authStore.userLogin();
};
</script>
