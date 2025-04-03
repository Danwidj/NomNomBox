<template>
  <header class="fixed-navbar">
    <div class="nom-container navbar-container">
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
              class="px-3 py-2 nom-nav-link rounded-md transition-colors group relative overflow-hidden"
              :class="{ 'active-nav-link': $route.path === '/' }"
            >
              <span class="relative z-10">Home</span>
              <!-- Hover background for inactive links -->
              <span v-if="$route.path !== '/'" class="absolute inset-0 bg-white/10 rounded-md scale-0 group-hover:scale-100 transition-transform duration-200 origin-center"></span>
              <!-- Active background that's always visible when route is active -->
              <span v-if="$route.path === '/'" class="absolute inset-0 bg-white/20 rounded-md"></span>
            </RouterLink>
            
            <RouterLink 
              to="/Product" 
              class="px-3 py-2 nom-nav-link rounded-md transition-colors group relative overflow-hidden"
              :class="{ 'active-nav-link': $route.path === '/Product' }"
            >
              <span class="relative z-10">Products</span>
              <span v-if="$route.path !== '/Product'" class="absolute inset-0 bg-white/10 rounded-md scale-0 group-hover:scale-100 transition-transform duration-200 origin-center"></span>
              <span v-if="$route.path === '/Product'" class="absolute inset-0 bg-white/20 rounded-md"></span>
            </RouterLink>
            
            <RouterLink 
              v-if="authState" 
              to="/Cart" 
              class="px-3 py-2 nom-nav-link rounded-md transition-colors group relative overflow-hidden"
              :class="{ 'active-nav-link': $route.path === '/Cart' }"
            >
              <span class="relative z-10 flex items-center">
                Shopping Cart
                <span 
                  v-if="cartItemCount > 0" 
                  class="ml-1.5 bg-white text-primary text-xs rounded-full h-5 min-w-5 flex items-center justify-center px-1 font-medium"
                  :class="{ 'cart-count-update': cartCountAnimating }"
                >
                  {{ cartItemCount }}
                </span>
              </span>
              <span v-if="$route.path !== '/Cart'" class="absolute inset-0 bg-white/10 rounded-md scale-0 group-hover:scale-100 transition-transform duration-200 origin-center"></span>
              <span v-if="$route.path === '/Cart'" class="absolute inset-0 bg-white/20 rounded-md"></span>
            </RouterLink>
            
            <RouterLink 
              to="/Chatbot" 
              class="px-3 py-2 nom-nav-link rounded-md transition-colors group relative overflow-hidden"
              :class="{ 'active-nav-link': $route.path === '/Chatbot' }"
            >
              <span class="relative z-10">Chatbot</span>
              <span v-if="$route.path !== '/Chatbot'" class="absolute inset-0 bg-white/10 rounded-md scale-0 group-hover:scale-100 transition-transform duration-200 origin-center"></span>
              <span v-if="$route.path === '/Chatbot'" class="absolute inset-0 bg-white/20 rounded-md"></span>
            </RouterLink>
            
            <RouterLink 
              v-if="authState" 
              to="/profile" 
              class="px-3 py-2 nom-nav-link rounded-md transition-colors group relative overflow-hidden"
              :class="{ 'active-nav-link': $route.path === '/profile' }"
            >
              <span class="relative z-10">Profile</span>
              <span v-if="$route.path !== '/profile'" class="absolute inset-0 bg-white/10 rounded-md scale-0 group-hover:scale-100 transition-transform duration-200 origin-center"></span>
              <span v-if="$route.path === '/profile'" class="absolute inset-0 bg-white/20 rounded-md"></span>
            </RouterLink>
          </nav>
        </div>

        <!-- Cart & Login/Logout -->
        <div class="flex items-center gap-3">
          <!-- Cart Icon with count (Mobile) -->
          <RouterLink 
            v-if="authState" 
            to="/Cart" 
            class="md:hidden relative p-2 text-primary-foreground hover:text-white transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
            <span 
              v-if="cartItemCount > 0" 
              class="absolute -top-1 -right-1 bg-white text-primary text-xs rounded-full h-5 min-w-5 flex items-center justify-center px-1 font-medium"
              :class="{ 'cart-count-update': cartCountAnimating }"
            >
              {{ cartItemCount }}
            </span>
          </RouterLink>

          <!-- Login/Logout Button with hover effect -->
          <button 
            @click="handleAuth" 
            class="bg-white/90 hover:bg-white text-primary px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200 shadow-sm hover:shadow-md group relative overflow-hidden"
          >
            <span class="relative z-10">{{ authState ? "Logout" : "Login" }}</span>
            <span class="absolute inset-0 bg-white opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
          </button>
        </div>
      </div>
    </div>
  </header>
  <!-- Add spacer to prevent content from hiding under fixed navbar -->
  <!-- <div class="h-16"></div> -->
</template>

<script>
import { ref, onMounted, watch, inject } from "vue";
import { useRouter, useRoute } from "vue-router";
import { isAuthenticated, logout, initAuth } from "@/stores/auth"; 

export default {
  name: 'Navbar',
  emits: ['cart-updated'],
  
  setup(props, { emit }) {
    const router = useRouter();
    const route = useRoute();
    const authState = ref(false);
    const cartItemCount = ref(0);
    const cartCountAnimating = ref(false);
    const previousCartCount = ref(0);
    
    // Initialize auth state when component mounts
    onMounted(() => {
      initAuth();
      authState.value = isAuthenticated.value;
      updateCartCount();
      
      // Listen for cart updates from other components
      window.addEventListener('cartUpdated', () => {
        updateCartCount(true);
      });
      
      // Also listen for storage events (for when cart is updated in another tab)
      window.addEventListener('storage', (event) => {
        if (event.key === 'shoppingCart') {
          updateCartCount(true);
        }
      });
      
      // Set up a polling mechanism to check the cart regularly
      // This is a fallback in case events are missed
      setInterval(() => updateCartCount(false), 5000);
    });
    
    // Watch for changes in the global auth state
    watch(() => isAuthenticated.value, (newValue) => {
      authState.value = newValue;
      if (newValue) {
        updateCartCount();
      } else {
        cartItemCount.value = 0;
        previousCartCount.value = 0;
      }
    });

    const updateCartCount = (animate = false) => {
      if (!authState.value) return;
      
      const cartData = sessionStorage.getItem('shoppingCart');
      
      if (cartData) {
        try {
          const cart = JSON.parse(cartData);
          // Calculate total items by summing up quantities
          const newCount = cart.reduce((total, item) => total + (item.quantity || 1), 0);
          
          // Only animate if count has changed and animation is requested
          if (newCount !== previousCartCount.value && animate) {
            cartCountAnimating.value = true;
            setTimeout(() => {
              cartCountAnimating.value = false;
            }, 500);
          }
          
          cartItemCount.value = newCount;
          previousCartCount.value = newCount;
        } catch (e) {
          console.error('Error parsing cart data:', e);
          cartItemCount.value = 0;
        }
      } else {
        cartItemCount.value = 0;
        previousCartCount.value = 0;
      }
    };

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
      route,
      cartItemCount,
      cartCountAnimating
    };
  }
};
</script>

<style scoped>
/* Fixed navbar styles */
.fixed-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  width: 100%;
  background-color: hsl(var(--primary) / 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid hsl(var(--border) / 0.4);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Cart update animation */
.cart-count-update {
  animation: pulse 0.5s ease-in-out;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.navbar-container {
  width: 100%;
  max-width: 100%;
  padding-right: var(--space-4);
  padding-left: var(--space-4);
}

@media (min-width: 640px) {
  .navbar-container {
    padding-right: var(--space-6);
    padding-left: var(--space-6);
  }
}

@media (min-width: 1024px) {
  .navbar-container {
    padding-right: var(--space-8);
    padding-left: var(--space-8);
  }
}

/* Active nav links */
.active-nav-link {
  font-weight: 500;
  color: hsl(var(--primary-foreground)) !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.active-nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40%;
  height: 2px;
  background-color: hsl(var(--primary-foreground));
  border-radius: 1px;
}
</style>