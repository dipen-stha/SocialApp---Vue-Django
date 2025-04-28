import { ref } from "vue";
import apiClient from "@/api/client";
import { authAPI } from "@/core/endpoints";
import jwtServices from "@/services/jwt";
import { acceptHMRUpdate, defineStore } from "pinia";
import router from "@/router";
import { toast } from "vue3-toastify";

export const useAuthStore = defineStore("auth", () => {
  const loginPayload = ref({
    email: "",
    password: "",
  });
  const signUpPayload = ref({
    email: "",
    name: "",
    password: "",
    repeat_password: "",
  })
  const loginError = ref(false);
  const signUpErrors = ref(null);

  const userLogin = async () => {
    try {
      const response = await apiClient.post(authAPI.login, loginPayload.value);
      if (response.data) {
        jwtServices.setToken(response.data.access);
        jwtServices.setRefreshToken(response.data.refresh);
        loginError.value = false;
        router.push({ name: "feed" });
        toast.success("Login Successful")
      }
    } catch (error) {
      loginError.value = true;
    }
  };

  const userSignUp = async () => {
    try{
      const response = await apiClient.post(authAPI.signup, signUpPayload.value)
      jwtServices.setToken(response.data.tokens.access);
      jwtServices.setRefreshToken(response.data.tokens.refresh);
      signUpErrors.value = null;
      router.push({ name: "feed" });
    } catch (error){
      signUpErrors.value = error.response.data;
    }
  }

  const userLogout = () => {
    jwtServices.destroyToken();
    router.push({ name: "login" });
  };

  const refreshToken = async (refresh) => {
    try {
      const response = await apiClient.post(authAPI.refresh, {
        refresh: refresh,
      });
      if (response.data) {
        jwtServices.setToken(response.data.access);
        jwtServices.setRefreshToken(response.data.refresh);
      }
    } catch (error) {}
  };

  return {
    loginPayload,
    signUpPayload,
    loginError,
    signUpErrors,
    userLogin,
    userSignUp,
    userLogout,
    refreshToken,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}
