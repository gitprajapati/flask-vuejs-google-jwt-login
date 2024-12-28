<template>
  <div class="login-page">
    <h1>Login</h1>
    <button @click="loginWithGoogle">Login with Google</button>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        error: null,
      };
    },
    methods: {
      loginWithGoogle() {
        window.location.href = "http://127.0.0.1:5000/auth/google";
      },
    },
  };
</script>
