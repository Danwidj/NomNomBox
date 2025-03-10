<template>
  <Navbar />
  <RouterView />
  <FooterComponent />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import FooterComponent from './components/FooterComponent.vue';
/* import HelloWorld from './components/HelloWorld.vue' */
</script>

