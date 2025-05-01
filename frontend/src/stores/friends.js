import apiClient from "@/api/client";
import { friendsAPI } from "@/core/endpoints";
import { defineStore } from "pinia";
import { ref } from "vue";
import { toast } from "vue3-toastify";

export const useFriendStore = defineStore("friend", () => {
    const friendsRequestsList = ref([]);
    const friendsList = ref([]);

    const fetchFriends = async (id) => {
        try {
            const response = await apiClient.get(friendsAPI.friendsList(id))
            friendsList.value = response.data
        } catch (error){

        }
    }

    const fetchFriendRequest = async () => {
        try{
            const response = await apiClient.get(friendsAPI.listRequests)
            friendsRequestsList.value = response.data
        } catch (error) {

        }
    }
    
    const sendFriendRequest = async (userId) => {
        try {
            const response = await apiClient.post(friendsAPI.sendRequest, {
                created_for: userId
            })
            if(response.data){
                toast.success("Friend Request Sent!")
            }
        } catch (error) {
            toast.error("Error sending friend request")
        }
    }

    const updateFriendRequest = async (id, status) => {
        try {
            const response = await apiClient.put(friendsAPI.updateRequest(id), {
                status: status
            })
        } catch (error) {
            toast.error("Error sending friend request")
        }
    }

    const reset = () => {
        friendsRequestsList.value = []
        friendsList.value = []
    }

    return {
        friendsList,
        friendsRequestsList,
        fetchFriends,
        fetchFriendRequest,
        sendFriendRequest,
        updateFriendRequest,
        reset
    }
})