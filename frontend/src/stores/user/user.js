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
  const self = reactive({
    id: null,
    name: null,
    email: null,
    avatar: null
  });
  const userRecommendations = ref([])
  const userStats = ref({
    friends_count: null,
    posts_count: null
  });

  const fetchSelfDetail = async () => {
    try {
      const response = await apiClient.get(authAPI.self);
      if (response.data) {
        isAuthenticated.value = true;
        self.id = response.data.id;
        self.name = response.data.name;
        self.email = response.data.email;
        self.avatar = response.data.avatar;
      }
    } catch (error) {
      isAuthenticated.value = false;
      throw error;
    }
  };

  const fetchUserDetail = async (id) => {
    try {
      const response = await apiClient.get(userAPI.userDetail(id));
      if (response.data) {
        isAuthenticated.value = true;
        user.id = response.data.id;
        user.name = response.data.name;
        user.email = response.data.email;
        user.avatar = response.data.avatar;
      }
    } catch (error) {
      isAuthenticated.value = false;
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

  const fetchUserStats = async (id) => {
    try {
      const response = await apiClient.get(userAPI.userStats(id))
      userStats.value.friends_count = response.data.friends_count
      userStats.value.posts_count = response.data.posts_count
    } catch (error){

    }
  }

  const reset = () => {
    user.value = null;
    userRecommendations.value = [];
    userStats.friends_count = null;
    userStats.posts_count = null;
  }

  return {
    isAuthenticated,
    user,
    self,
    userRecommendations,
    userStats,
    fetchUserDetail,
    fetchUserRecommendations,
    fetchSelfDetail,
    fetchUserStats,
    reset
  };
});
