import { defineStore } from "pinia";
import { ref } from "vue";
import apiClient from "@/api/client";
import { authAPI } from "@/core/endpoints";

export const useUserStore = defineStore("user", () => {
  
  const isAuthenticated = ref(false);
  const user = ref({
    id: ref(null),
    name: ref(null),
    email: ref(null),
  });

  const fetchUserDetail = async () => {
    try {
      const response = await apiClient.get(authAPI.self);
      if (response.data) {
        isAuthenticated.value = true;
        user.id = response.data[0].id;
        user.name = response.data[0].name;
        user.email = response.data[0].email;
      }
    } catch (error) {
      user.isAuthenticated = false;
      throw error;
    }
  };

  return {
    isAuthenticated,
    user,
    fetchUserDetail,
  };
});
