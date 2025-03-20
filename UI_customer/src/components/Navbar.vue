<template>
  <nav>
    <div class="nav-links">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/Product">Product</RouterLink>
      <RouterLink to="/Cart">Shopping Cart</RouterLink>
      <RouterLink to="/Chatbot">Chatbot</RouterLink>
      <RouterLink v-if="authState" to="/profile">Profile</RouterLink>
    </div>

    <!-- Login/Logout Button -->
    <button @click="handleAuth" class="auth-button">
      {{ authState ? "Logout" : "Login" }}
    </button>
  </nav>
</template>

<script>
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { isAuthenticated, logout, initAuth } from "@/stores/auth"; 

export default {
  setup() {
    const router = useRouter();
    const authState = ref(false);
    
    // Initialize auth state when component mounts
    onMounted(() => {
      initAuth();
      authState.value = isAuthenticated.value;
    });
    
    // Watch for changes in the global auth state
    watch(() => isAuthenticated.value, (newValue) => {
      authState.value = newValue;
    });

    const handleAuth = () => {
      if (authState.value) {
        logout();
        router.push("/login");
      } else {
        router.push("/login");
      }
    };

    return { 
      authState,
      handleAuth 
    };
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