export const authAPI = {
    login: "account/authenticate/login/",
    signup: "account/authenticate/signup/",
    refresh: "account/authenticate/refresh/",
    self: "account/authenticate/self/user/"
}

export const userAPI = {
    userList: "account/user/",
    userDetail: (id) => `account/user/${id}`,
}

export const chatAPI = {
    chatList: "chat/conversation-message/"
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
}