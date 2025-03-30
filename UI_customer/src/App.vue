<template>
  <div class="flex flex-col min-h-screen bg-background">
    <Navbar />
    <main class="flex-grow">
      <RouterView />
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
}

/* Make sure Vite app container takes full space */
#app {
  margin: 0 !important;
  padding: 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>

<script setup>
import { onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
import FooterComponent from './components/FooterComponent.vue';
import { initAuth } from '@/stores/auth';

// Initialize auth state when the app loads
onMounted(() => {
  initAuth();
});
</script>