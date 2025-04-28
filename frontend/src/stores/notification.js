import apiClient from "@/api/client";
import { notificationAPI } from "@/core/endpoints";
import { defineStore } from "pinia";
import { ref } from 'vue';

export const useNotificationStore = defineStore("notification" ,() => {
    const notificationList = ref([]);
    const notificationStats = ref(null);

    const fetchNotificationList = async() => {
        try {
            const response = await apiClient.get(notificationAPI.notificationList)
            notificationList.value = response.data
        } catch (error) {

        }
    }
    
    const fetchNotificationStats = async() => {
        try{
            const response = await apiClient.get(notificationAPI.notificationStats)
            notificationStats.value = response.data
        } catch (error){

        }
    }
    return {
        notificationList,
        notificationStats,
        fetchNotificationList,
        fetchNotificationStats
    }
})