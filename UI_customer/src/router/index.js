import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Cart from '../views/Cart.vue'
import Product from '../views/Product.vue'
import Profile from '../views/Profile.vue'
import Chatbot from '../views/Chatbot.vue'
import EditProfile from '../views/EditProfile.vue'
import AuthView from '@/views/AuthView.vue'
import SignUpView from '@/views/SignUpView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/product',
      name: 'product',
      component: Product,
    },
    {
      path: '/cart',
      name: 'cart',
      component: Cart,
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: Chatbot,
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true }, // Protected Route
    },
    {
      path: '/edit-profile',
      name: 'edit-profile',
      component: EditProfile,
      meta: { requiresAuth: true }, // Protected Route
    },
    {
      path: '/login',
      name: 'auth',
      component: AuthView,
      meta: { requiresGuest: true }, // Prevent logged-in users from accessing
    },
    {
      path: '/signup',
      name: 'sign-up',
      component: SignUpView,
      meta: { requiresGuest: true }, // Prevent logged-in users from accessing
    },
  ],
})

// 🔹 **Navigation Guard for Authentication**
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token'); // Get stored token

  if (to.meta.requiresAuth && !token) {
    // If user is not logged in and tries to access a protected page
    next('/login'); // Redirect to login
  } else if (to.meta.requiresGuest && token) {
    // If user is logged in and tries to access login/signup
    next('/profile'); // Redirect to profile
  } else {
    next(); // Allow navigation
  }
});

export default router;
