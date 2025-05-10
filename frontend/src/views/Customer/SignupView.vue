<template>
    <div class="primary-background h-screen">
      <div class="h-screen flex justify-center items-center">
        <div class="min-h-[500px] min-w-[400px] primary-background rounded-md shadow-lg">
          <div class="text-center mt-[30px]">
            <span class="text-xl font-semibold">Login</span>
          </div>
          <form class="mt-[15px]" @submit.prevent="onSignUp">
            <div class="flex h-full justify-center items-center">
              <div class="flex flex-col gap-y-[15px] w-[90%]">
                <div
                  class="flex flex-col gap-y-[10px] border primary-border p-4 rounded-md"
                >
                  <div class="flex flex-col justify-center">
                    <input
                      type="text"
                      class="input-field w-full text-stone-900"
                      placeholder="Enter Email"
                      v-model="signUpPayload.email"
                    />
                    <div v-if="signUpErrors?.email">
                      <span class="error">{{ signUpErrors.email[0] }}</span>
                    </div>
                  </div>
                  <div class="flex flex-col justify-center">
                    <input
                      type="text"
                      class="input-field w-full text-stone-900"
                      placeholder="Enter Name"
                      v-model="signUpPayload.name"
                    />
                    <div v-if="signUpErrors?.name">
                      <span class="error">{{ signUpErrors.name[0] }}</span>
                    </div>
                  </div>
                  <div class="flex flex-col justify-center">
                    <input
                      type="password"
                      class="input-field w-full text-stone-900"
                      placeholder="Enter Password"
                      v-model="signUpPayload.password"
                    />
                    <div v-if="signUpErrors?.password">
                      <span class="error">{{ signUpErrors.password[0] }}</span>
                    </div>
                  </div>
                  <div class="flex flex-col justify-center">
                    <input
                      type="password"
                      class="input-field w-full text-stone-900"
                      placeholder="Repeat Password"
                      v-model="signUpPayload.repeat_password"
                    />
                    <div v-if="signUpErrors?.repeat_password">
                      <span class="error">{{ signUpErrors.repeat_password[0] }}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <button
                    type="submit"
                    class="w-full bg-slate-500 p-2 rounded-md text-white"
                  >
                    Sign Up
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
  import { ref, onUnmounted } from "vue";
  import { storeToRefs } from "pinia";
  
  const authStore = useAuthStore();
  const userStore = useUserStore();
  
  const { signUpPayload, signUpErrors } = storeToRefs(authStore);
  
  const onSignUp = async () => {
    await authStore.userSignUp();
  };

  onUnmounted(async () => {
    authStore.$dispose
  });
  </script>
  