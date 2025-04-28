<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="bg-white p-4 mb-6 rounded border border-gray-200">
                <div class="my-4">
                    <ul>
                        <li v-for="chat in chats" :key="chat.id" class="mb-4">
                            <div v-for="chatUser in chat.users" >
                                <div v-if="user.id !== chatUser.id"  class="flex justify-between items-center space-x-2 cursor-pointer" @click="fetchConvo(chat.id, chatUser.id)">
                                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjYaK0N_g8erthyNgnhxn8dse9ImHEXm6gpw&s" class="rounded-full h-10 w-10"/>
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
            <div class="bg-white border border-gray-200 rounded-lg">
                <div class="flex flex-col flex-grow p-4">
                    <div v-for="message in messages">
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
            <div class="bg-white border border-gray-200 rounded-lg">
                <div class="flex justify between p-4">
                    <div class="w-full">
                        <textarea class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Write your message" v-model="textMessage"></textarea>
                    </div>
                    <div>
                        <button @click="sendMessage" class="px-4 mx-3 py-2 bg-purple-500 hover:bg-purple-700 rounded-lg text-white">Send</button>
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

const chats = ref(null)

const messages = ref(null)

const textMessage = ref(null)

const userStore = useUserStore();

const conversationSelected = ref(false);

const conversationDetails = reactive({
    id: '',
    sent_to: ''
})

let socket = null;

const user = userStore.user

const fetchChats = async () => {
    const response = await axios.get('api/chat/conversation/')
    chats.value = response.data
}

const fetchConvo = async (chatId, chatUser) => {
    try {
        console.log(chatId, chatUser)
        const response = await axios.get(`api/chat/conversation-message/`)
        messages.value = response.data
        conversationSelected.value = true
        conversationDetails.id = chatId
        conversationDetails.sent_to = chatUser

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
        console.log(conversationDetails.id, conversationDetails.sent_to)
        const response = await axios.post('api/chat/conversation-message/', {
            "message": textMessage.value,
            "conversation": conversationDetails.id,
            "sent_to": conversationDetails.sent_to,
        })
        if(response.data){
            messages.value.push(response.data)
            textMessage.value = ''
        }
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
    fetchChats()
    connectChatSocket()
})
</script>