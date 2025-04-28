import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/signup",
      name: "signup",
      component: () => import("@/views/SignupView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/LoginView.vue"),
    },
    {
      path: "/",
      name: "authLayout",
      component: () => import("@/Layout/AuthLayout.vue"),
      children: [
        {
          path: "/feed",
          name: "feed",
          component: () => import("@/views/FeedView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/search",
          name: "search",
          component: () => import("@/views/SearchView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/profile/:id",
          name: "profile",
          component: () => import("@/views/ProfileView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/profile/:id/friends",
          name: "friends",
          component: () => import("@/views/FriendsView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/:id/",
          name: "postdetail",
          component: () => import("@/views/PostDetailView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/chat",
          name: "chat",
          component: () => import("@/views/ChatView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/about",
          name: "about",
          component: () => import("../views/AboutView.vue"),
          meta: { requiresAuth: true },
        },
      ],
    },
  ],
});

export default router;
