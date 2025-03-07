<template>
  <nav>
    <div class="flex">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/Product">Product</RouterLink>
      <RouterLink to="/Cart">Shopping Cart</RouterLink>
      <RouterLink to="/Profile">Profile</RouterLink>
    </div>
  </nav>

</template>

<script setup>
import { RouterLink } from 'vue-router'
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from '@/components/ui/navigation-menu'

</script>

<style scoped>
nav {
  width: 100%;
  font-size: 14px;
  display: flex;
  justify-content: center;
  background-color: #000000;
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