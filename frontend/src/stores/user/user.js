import { defineStore } from "pinia";
import { ref, reactive } from "vue";
import apiClient from "@/api/client";
import { authAPI, userAPI } from "@/core/endpoints";

export const useUserStore = defineStore("user", () => {
  
  const isAuthenticated = ref(false);
  const user = reactive({
    id: null,
    name: null,
    email: null,
    avatar: null
  });
  const userRecommendations = ref([])

  const fetchUserDetail = async () => {
    try {
      const response = await apiClient.get(authAPI.self);
      if (response.data) {
        isAuthenticated.value = true;
        user.id = response.data.id;
        user.name = response.data.name;
        user.email = response.data.email;
        user.avatar = response.data.avatar;
      }
    } catch (error) {
      user.isAuthenticated = false;
      throw error;
    }
  };

  const fetchUserRecommendations = async() => {
    try{
      const response = await apiClient.get(userAPI.userList, {
        params: {
          type: 'recommendations'
        }
      })
      userRecommendations.value = response.data
    } catch (error){

    }
  }

  return {
    isAuthenticated,
    user,
    userRecommendations,
    fetchUserDetail,
    fetchUserRecommendations
  };
});
