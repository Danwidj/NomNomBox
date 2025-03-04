<template>
  <nav>
    <RouterLink to="/">Home</RouterLink>
    <RouterLink to="/recipes">Recipes</RouterLink>
    <RouterLink to="/plans">Plans</RouterLink>
    <RouterLink to="/contact">Contact</RouterLink>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
nav {
  width: 100%;
  font-size: 14px;
  display: flex;
  justify-content: center;
  background-color: #f8f9fa;
  padding: 1rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid #ddd;
}

nav a:first-of-type {
  border: 0;
}

nav a.router-link-exact-active {
  color: #007bff;
}
</style>