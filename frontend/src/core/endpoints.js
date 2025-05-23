export const authAPI = {
    login: "account/authenticate/login/",
    signup: "account/authenticate/signup/",
    refresh: "account/authenticate/refresh/",
    self: "account/authenticate/self/user/",
    verify: (token) => `account/authenticate/verify/${token}/`
}

export const userAPI = {
    userList: "account/user/",
    userDetail: (id) => `account/user/${id}/`,
    userStats: (id) => `account/user/stats/${id}/`
}

export const chatAPI = {
    chatList: "chat/conversation/",
    conversationList: "chat/conversation-message/",
    conversationDetail: (id) => `chat/conversation-message/${id}` ,
    sendMessage: "chat/conversation-message/"
}

export const notificationAPI = {
    notificationList: "notification/list-notifications",
    notificationStats: "notification/get-stats/"
}

export const postAPI = {
    fetchPostList: "posts/",
    postDetail: (id) => `posts/${id}/`,
    postCreate: "posts/",
    postUpdate: (id) => `posts/${id}/`,
    addComment: (id) => `posts/${id}/add_comments/`,
    addLikes: (id) => `posts/${id}/add_likes/`,
    search: 'posts/search/'
}

export const friendsAPI = {
    friendsList: (id) => `friends/list/${id}`,
    sendRequest: 'friends/friend-requests/',
    updateRequest: (id) => `friends/friend-requests/${id}/`,
    listRequests: 'friends/friend-requests/' 
}