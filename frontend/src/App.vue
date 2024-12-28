<template>
  <div id="app">
    <LoginPage v-if="!isAuthenticated" />
    <div v-else>
      <h1>Welcome, {{ user.email }}</h1>
      <p>Role: {{ user.role }}</p>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
  import LoginPage from "./components/LoginPage.vue";
  import { jwtDecode } from "jwt-decode";

  export default {
    data() {
      return {
        token: null,
        user: null,
      };
    },
    computed: {
      isAuthenticated() {
        return !!this.user;
      },
    },
    created() {
      this.initializeAuth();
    },
    methods: {
      initializeAuth() {
        console.log("Initializing Authentication...");

        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get("token");
        console.log("Token from URL:", token);

        if (token) {
          try {
            localStorage.setItem("token", token);
            console.log("Token saved to localStorage.");
            window.history.replaceState({}, document.title, "/");
          } catch (e) {
            console.error("Error saving token to localStorage:", e);
          }
        }

        this.token = localStorage.getItem("token");
        console.log("Token from localStorage:", this.token);

        if (this.token) {
          try {
            const decoded = jwtDecode(this.token);
            console.log("Decoded Token:", decoded);

            if (
              decoded &&
              decoded.sub &&
              decoded.sub.email &&
              decoded.sub.role
            ) {
              this.user = {
                email: decoded.sub.email,
                role: decoded.sub.role,
              };
              console.log("User Info:", this.user);
              this.routeUser(decoded.sub.role);
            } else {
              console.error("Token is missing email or role data in sub.");
              this.logout();
            }
          } catch (e) {
            console.error("Invalid Token:", e);
            this.logout();
          }
        } else {
          console.log("No token found, showing login page.");
        }
      },
      routeUser(role) {
        if (this.$router) {
          if (role === "admin") {
            console.log("Routing to /admin");
            this.$router.push("/admin");
          } else if (role === "user") {
            console.log("Routing to /user");
            this.$router.push("/user");
          }
        } else {
          console.error("Router instance is not available.");
        }
      },
      logout() {
        localStorage.removeItem("token");
        this.user = null;
        this.token = null;
        console.log("Logged out, redirecting to login.");
        if (this.$router) {
          this.$router.push("/");
        }
      },
    },
    components: {
      LoginPage,
    },
  };
</script>
