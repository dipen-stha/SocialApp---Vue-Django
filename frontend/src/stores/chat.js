import apiClient from "@/api/client";
import { chatAPI } from "@/core/endpoints";
import { defineStore } from "pinia";
import { reactive, ref } from "vue";

export const useChatStore = defineStore("chat", () => {
    const chatList = ref([]);
    const conversationMesssagelist = ref([]);
    const messagePayload = reactive({
        message: null,
        conversation: null,
        sent_to: null

    })

    const fetchChatList = async () => {
        try{
            const response = await apiClient.get(chatAPI.chatList)
            chatList.value = response.data
        } catch (error) {

        }
    };

    const fetchConversationMessages = async () => {
        try{
            const response = await apiClient.get(chatAPI.conversationList)
            conversationMesssagelist.value = response.data
        } catch (error) {

        }
    }

    const sendMessage = async () => {
        try {
            const response = await apiClient.post(chatAPI.sendMessage, messagePayload)
            if(response.data){
                conversationMesssagelist.value.push(response.data)
                messagePayload.message = null;
            }
        } catch (error) {

        }
    }

    const reset = () => {
        chatList.value = []
        conversationMesssagelist.value = []
    }
    return {
        chatList,
        conversationMesssagelist,
        messagePayload,
        fetchChatList,
        fetchConversationMessages,
        sendMessage,
        reset
    }
})