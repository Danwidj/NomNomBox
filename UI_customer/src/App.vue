<template>
  <Navbar />
  <RouterView />
  <FooterComponent />
</template>

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