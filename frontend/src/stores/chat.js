import apiClient from "@/api/client";
import { chatAPI } from "@/core/endpoints";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useChatStore = defineStore("chat", () => {
    const chatList = ref([]);

    const fetchChatList = async () => {
        try{
            const response = await apiClient.get(chatAPI.chatList)
            chatList.value = response.data
        } catch (error) {

        }
    };
    return {
        chatList,
        fetchChatList,
    }
})