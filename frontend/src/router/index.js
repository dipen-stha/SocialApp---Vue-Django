import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/signup",
      name: "signup",
      component: () => import("@/views/Customer/SignupView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/Customer/LoginView.vue"),
    },
    {
      path: "/",
      name: "authLayout",
      component: () => import("@/Layout/AuthLayout.vue"),
      meta: { requiresAuth: true },
      children: [
        {
          path: "/feed",
          name: "feed",
          component: () => import("@/views/Customer/FeedView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/search",
          name: "search",
          component: () => import("@/views/Customer/SearchView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/profile/:id",
          name: "profile",
          component: () => import("@/views/Customer/ProfileView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/profile/:id/friends",
          name: "friends",
          component: () => import("@/views/Customer/FriendsView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/:id/",
          name: "postdetail",
          component: () => import("@/views/Customer/PostDetailView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/chat",
          name: "chat",
          component: () => import("@/views/Customer/ChatView.vue"),
          meta: { requiresAuth: true },
        },
        {
          path: "/about",
          name: "about",
          component: () => import("../views/Customer/AboutView.vue"),
          meta: { requiresAuth: true },
        },
      ],
    },
    {
      path: '/admin',
      name: 'adminAuthLayout',
      component: () => import("../Layout/AdminAuthLayout.vue"),
      meta: { requiresAuth: false },
      children: [
        {
          path: "/dashboard",
          name: "dashboard",
          component: () => import("../views/Dashboard/Index.vue"),
          meta: {requiresAuth: false}
        },
        {
          path: "/user",
          name: "user",
          component: () => import("../views/Dashboard/Users/User.vue"),
          meta: {
            requiresAuth: false
          }
        }
      ]
    },
  ],
});

export default router;
