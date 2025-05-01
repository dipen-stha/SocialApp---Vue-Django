<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="primary-background p-4 mb-6 rounded border primary-border primary-text">
                <div class="my-4">
                    <ul>
                        <li v-for="chat in chatList" :key="chat.id" class="mb-4">
                            <div v-for="chatUser in chat.users" >
                                <div v-if="user.id !== chatUser.id"  class="flex justify-between items-center space-x-2 cursor-pointer" @click="fetchConvo(chat.id, chatUser.id)">
                                    <img :src="chatUser.avatar" class="h-10 w-10 rounded-full"/>
                                    <p class="text-xs truncate ... font-semibold">{{ chatUser.name }}</p>
                                    <p class="text-xs text-gray-500">{{ chat.formatted_modified_at }}</p>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>  
        <div v-if="conversationSelected" class="main-right col-span-3">
            <div class="h-[600px] overflow-y-auto scroll-hidden primary-background primary-border rounded-lg">
                <div class="flex flex-col flex-grow p-4">
                    <div v-for="message in conversationMesssagelist">
                        <div v-if="message.created_by.id == user.id" class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                            <div>
                                <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                    <p>{{ message.message }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{ timeAgo(message.created_at)}}</span>
                            </div>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img :src="message.created_by.avatar" class="rounded-full w-[40px]"/>
                            </div>
                        </div>
                        <div v-else class="flex w-full mt-2 space-x-3 max-w-md mr-auto">
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img :src="message.created_by.avatar" class="rounded-full w-[40px]"/>
                            </div>
                            <div>
                                <div class="bg-gray-200 text-gray-800 p-3 rounded-r-lg rounded-bl-lg">
                                    <p>{{ message.message }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{ message.conversation.formatted_modified_at }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="primary-background primary-border rounded-lg">
                <div class="flex justify-between p-4">
                    <div class="w-full">
                        <textarea class="p-4 w-full primary-background primary-border rounded-lg focus:outline-none primary-text" placeholder="Write your message" v-model="messagePayload.message"></textarea>
                    </div>
                    <div>
                        <button @click="sendMessage" class="px-4 mx-3 py-2 btn-primary">Send</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user/user';
import axios from 'axios';
import { onMounted, ref, computed, onBeforeUnmount,reactive } from 'vue';
import { timeAgo } from '@/utils/timeAgo';
import { useChatStore } from '@/stores/chat';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const chatStore = useChatStore();

const conversationSelected = ref(false);

const { chatList, conversationMesssagelist, messagePayload } = storeToRefs(chatStore)

let socket = null;

const user = userStore.self

const fetchConvo = async (chatId, chatUser) => {
    try {
        chatStore.fetchConversationMessages();
        conversationSelected.value = true
        messagePayload.value.conversation = chatId
        messagePayload.value.sent_to = chatUser

    } catch (error) {
        console.log(error)
        conversationSelected.value = false
    }
}

const connectChatSocket = async () => {
    const socketUrl = 'ws://localhost:8000/ws/chat/'
    socket = new WebSocket(socketUrl);

    socket.onopen = () => {
        console.log('Chat socket connected')
    }

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        fetchConvo(data.data.id, data.data.sent_to)
    }
}

const sendMessage = async(chatId) => {
    try{
        chatStore.sendMessage();
    } catch(error){
        console.log(error)
    }
}

onBeforeUnmount(() => {
  if (socket) {
    socket.close();
  }
});

onMounted(() => {
    chatStore.fetchChatList();
    connectChatSocket();
})
</script>