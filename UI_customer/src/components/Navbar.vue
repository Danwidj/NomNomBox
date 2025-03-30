<template>
  <header class="nom-navbar">
    <div class="nom-container">
      <div class="flex h-16 items-center justify-between">
        <!-- Logo and Navigation Links -->
        <div class="flex items-center gap-8">
          <RouterLink to="/" class="text-xl font-bold text-primary-foreground hover:opacity-90 transition-all duration-200 flex items-center gap-2">
            <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L15 8H9L12 2Z" fill="currentColor" />
              <path d="M19 10C19 13.866 15.866 17 12 17C8.13401 17 5 13.866 5 10H19Z" fill="currentColor" />
              <path d="M5 20C5 18.3431 6.34315 17 8 17H16C17.6569 17 19 18.3431 19 20C19 21.6569 17.6569 23 16 23H8C6.34315 23 5 21.6569 5 20Z" fill="currentColor" />
            </svg>
            NomNomBox
          </RouterLink>
          
          <nav class="hidden md:flex items-center space-x-1">
            <RouterLink 
              to="/" 
              class="px-3 py-2 nom-nav-link rounded-md transition-colors"
              :class="{ 'text-primary-foreground font-medium': $route.path === '/' }"
            >
              Home
            </RouterLink>
            
            <RouterLink 
              to="/Product" 
              class="px-3 py-2 nom-nav-link rounded-md transition-colors"
              :class="{ 'text-primary-foreground font-medium': $route.path === '/Product' }"
            >
              Products
            </RouterLink>
            
            <RouterLink 
              v-if="authState" 
              to="/Cart" 
              class="px-3 py-2 nom-nav-link rounded-md transition-colors"
              :class="{ 'text-primary-foreground font-medium': $route.path === '/Cart' }"
            >
              Shopping Cart
            </RouterLink>
            
            <RouterLink 
              to="/Chatbot" 
              class="px-3 py-2 nom-nav-link rounded-md transition-colors"
              :class="{ 'text-primary-foreground font-medium': $route.path === '/Chatbot' }"
            >
              Chatbot
            </RouterLink>
            
            <RouterLink 
              v-if="authState" 
              to="/profile" 
              class="px-3 py-2 nom-nav-link rounded-md transition-colors"
              :class="{ 'text-primary-foreground font-medium': $route.path === '/profile' }"
            >
              Profile
            </RouterLink>
          </nav>
        </div>

        <!-- Login/Logout Button -->
        <button 
          @click="handleAuth" 
          class="bg-white/90 hover:bg-white text-primary px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200 shadow-sm hover:shadow"
        >
          {{ authState ? "Logout" : "Login" }}
        </button>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { isAuthenticated, logout, initAuth } from "@/stores/auth"; 

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter();
    const route = useRoute();
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
      handleAuth,
      route
    };
  }
};
</script>