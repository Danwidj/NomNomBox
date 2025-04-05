<template>
  <div class="flex flex-col min-h-screen bg-background">
    <Navbar @cart-updated="handleCartUpdate" />
    <main class="flex-grow">
      <RouterView @cart-updated="handleCartUpdate" />
    </main>
    <FooterComponent />
  </div>
</template>

<style>
/* Reset default margins and paddings */
html, body {
  margin: 0;
  padding: 0;
  min-height: 100%;
  height: 100%;
  width: 100%;
  overflow-x: hidden;
}

/* Make sure Vite app container takes full space */
#app {
  margin: 0 !important;
  padding: 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  position: relative;
}

/* Add to cart animation */
@keyframes ripple {
  from {
    opacity: 1;
    transform: scale(0);
  }
  to {
    opacity: 0;
    transform: scale(2);
  }
}

.add-to-cart-ripple {
  animation: ripple 0.7s ease-out;
}

/* Cart Count Animation */
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

.cart-count-update {
  animation: pulse 0.5s ease-in-out;
}

/* Custom scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: hsl(var(--muted));
  border-radius: 8px;
}

::-webkit-scrollbar-thumb {
  background: hsl(var(--primary));
  border-radius: 8px;
}

::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--primary) / 0.8);
}

/* Firefox scrollbar */
* {
  scrollbar-width: thin;
  scrollbar-color: hsl(var(--primary)) hsl(var(--muted));
}

/* Fix for layout shifting */
html {
  overflow-y: scroll;
  scroll-behavior: smooth;
}

/* Fix for container width consistency */
.nom-container {
  box-sizing: border-box;
  width: 100%;
}

/* Prevent layout shift */
.fixed-layout {
  overflow-x: hidden;
  width: 100%;
}

/* Main content area with proper padding for fixed navbar */
main {
  margin-top: 64px; /* Same as navbar height */
  width: 100%;
  box-sizing: border-box;
}
</style>

<script setup>
import { onMounted, provide } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
import FooterComponent from './components/FooterComponent.vue';
import { initAuth } from '@/stores/auth';

// Function to handle cart updates and trigger events
const handleCartUpdate = () => {
  // Create a custom event that components can listen for
  const event = new CustomEvent('cartUpdated');
  window.dispatchEvent(event);
  
  // Also update sessionStorage to trigger the storage event
  const cart = JSON.parse(sessionStorage.getItem('shoppingCart') || '[]');
  sessionStorage.setItem('shoppingCart', JSON.stringify(cart));
};

// Make the cart update handler available to all components
provide('cartUpdateHandler', handleCartUpdate);

// Initialize auth state when the app loads
onMounted(() => {
  initAuth();
  
  // Force a layout recalculation to ensure navbar is properly positioned
  setTimeout(() => {
    window.dispatchEvent(new Event('resize'));
  }, 100);
});
</script>