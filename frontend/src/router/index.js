import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "@/components/LoginPage.vue";
import AdminDashboard from "@/components/AdminDashboard.vue";
import UserDashboard from "@/components/UserDashboard.vue";

const routes = [
  { path: "/", name: "Login", component: LoginPage },
  {
    path: "/admin",
    name: "Admin",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/user",
    name: "User",
    component: UserDashboard,
    meta: { requiresAuth: true, role: "user" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth) {
    if (!token) {
      console.warn("No token found, redirecting to login");
      next({ path: "/" });
    } else {
      try {
        const decoded = JSON.parse(atob(token.split(".")[1]));
        if (to.meta.role && decoded.identity.role !== to.meta.role) {
          console.warn(`Unauthorized role access: ${decoded.identity.role}`);
          next({ path: "/" });
        } else {
          next();
        }
      } catch (e) {
        console.error("Token validation error:", e);
        localStorage.removeItem("token");
        next({ path: "/" });
      }
    }
  } else {
    next();
  }
});

export default router;
