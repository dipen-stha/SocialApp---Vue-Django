import apiClient from "@/api/client";
import { postAPI } from "@/core/endpoints";
import { defineStore } from "pinia";
import { reactive, ref } from "vue";

export const usePostStore = defineStore("post", () => {
    const postList = ref([]);
    const postDetail = ref(null);
    const postPayload = reactive({
        body: null,
        attachments: []
    });
    
    const fetchPostList = async () => {
        try{
            const response = await apiClient.get(postAPI.fetchPostList)
            postList.value = response.data
        } catch (error) {

        }
    }

    const retrievePostDetail = async (id) => {
        try{
            const response = await apiClient.get(postAPI.postDetail)
            postDetail.value = response.data
        } catch (error){

        }
    }

    const createPost = async () => {
        try{
            const response = await apiClient.post(postAPI.postCreate, postPayload)
            if(response.data){
                postPayload.body = null;
                postPayload.attachments = [];
                postList.value.unshift(response.data);
            }
        } catch(error){

        }
    }

    const updatePost = async (id) => {
        try{
            const response = await apiClient.post(postAPI.postUpdate(id), postPayload.value)
            postList.value.unshift(response.data)

        } catch(error){

        }
    }
    
    const createComment = async (postId) => {
        try{
            const response = await apiClient.post(postAPI.addComment(postId))
            await fetchPostList();
        } catch (error){

        }
    }

    const createLikes = async(postId) => {
        try{
            const response = await apiClient.post(postAPI.addLikes(postId))
            await fetchPostList();
        } catch (error){
            
        }
    }

    return {
        postList,
        postDetail,
        postPayload,
        fetchPostList,
        retrievePostDetail,
        createPost,
        updatePost,
        createComment,
        createLikes,
    }
})