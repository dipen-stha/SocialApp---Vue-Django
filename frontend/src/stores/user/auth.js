import { ref } from "vue";
import apiClient from "@/api/client";
import { authAPI } from "@/core/endpoints";
import jwtServices from "@/services/jwt";
import { acceptHMRUpdate, defineStore } from "pinia";
import router from "@/router";

export const useAuthStore = defineStore("auth", () => {
  const loginPayload = ref({
    email: "",
    password: "",
  });
  const loginError = ref(false);

  const userLogin = async () => {
    try {
      const response = await apiClient.post(authAPI.login, loginPayload.value);
      if (response.data) {
        jwtServices.setToken(response.data.access);
        jwtServices.setRefreshToken(response.data.refresh);
        loginError.value = false;
        router.push({ name: "feed" });
      }
    } catch (error) {
      loginError.value = true;
    }
  };

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
    loginError,
    userLogin,
    userLogout,
    refreshToken,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}
