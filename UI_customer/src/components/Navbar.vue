<template>
  <nav>
    <div class="nav-links">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/Product">Product</RouterLink>
      <RouterLink to="/Cart">Shopping Cart</RouterLink>
      <RouterLink to="/Chatbot">Chatbot</RouterLink>
      <RouterLink to="/Profile">Profile</RouterLink>
    </div>

    <!-- Login/Logout Button -->
    <button @click="handleAuth" class="auth-button">
      {{ isAuthenticated ? "Logout" : "Login" }}
    </button>
  </nav>
</template>

<script>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { isAuthenticated, logout } from "@/stores/auth"; // Import global auth store

export default {
  setup() {
    const router = useRouter();

    const handleAuth = () => {
      if (isAuthenticated.value) {
        logout();
        router.push("/login"); // Redirect on logout
      } else {
        router.push("/login"); // Redirect to login
      }
    };

    return { isAuthenticated, handleAuth };
  },
};
</script>

<style scoped>
nav {
  width: 100%;
  font-size: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #000000;
  padding: 1rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.nav-links {
  display: flex;
  gap: 20px;
}

nav a {
  color: white;
  text-decoration: none;
  padding: 0 1rem;
  border-left: 1px solid #ddd;
}

nav a:first-of-type {
  border: 0;
}

nav a.router-link-exact-active {
  color: #007bff;
}

.auth-button {
  padding: 8px 16px;
  background-color: white;
  color: #000000;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.auth-button:hover {
  background-color: #ecf0f1;
}
</style>
