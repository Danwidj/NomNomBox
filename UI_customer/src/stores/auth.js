import { ref, watchEffect } from "vue";

export const isAuthenticated = ref(!!localStorage.getItem("token")); // Reactive state

export function login(token) {
  localStorage.setItem("token", token);
  isAuthenticated.value = true; // Ensure reactivity updates immediately
}

export function logout() {
  localStorage.removeItem("token");
  isAuthenticated.value = false; // Reactively update logout status
}

// Ensure `isAuthenticated` updates even if `localStorage` changes from another tab
watchEffect(() => {
  isAuthenticated.value = !!localStorage.getItem("token");
});
