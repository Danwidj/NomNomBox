import { ref } from "vue";

export const isAuthenticated = ref(!!localStorage.getItem("token")); // Reactive state

export function login(token) {
  localStorage.setItem("token", token);
}

export function logout() {
  localStorage.removeItem("token");
  isAuthenticated.value = false; // Reactively update logout status
}
