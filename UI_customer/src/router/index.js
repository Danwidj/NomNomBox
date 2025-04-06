import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Cart from '../views/Cart.vue'
import Product from '../views/Product.vue'
import Profile from '../views/Profile.vue'
import Chatbot from '../views/Chatbot.vue'
import EditProfile from '../views/EditProfile.vue'
import AuthView from '@/views/AuthView.vue'
import SignUpView from '@/views/SignUpView.vue'
import Success from "@/views/Success.vue"
import ScheduleDelivery from '@/views/ScheduleDelivery.vue'
import { isAuthenticated, initAuth } from '@/stores/auth'

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
      meta: { requiresAuth: true }, 
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: Chatbot,
    },
    {
      path: '/profile/:customerId?',
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true },
    },
    {
      path: '/edit-profile',
      name: 'edit-profile',
      component: EditProfile,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'auth',
      component: AuthView,
      meta: { requiresGuest: true },
    },
    {
      path: '/signup',
      name: 'sign-up',
      component: SignUpView,
      meta: { requiresGuest: true },
    },
    {
      path: '/success',
      name: 'success',
      component: Success,
    },
    {
      path: '/schedule-delivery/:orderId',
      name: 'ScheduleDelivery',
      component: ScheduleDelivery,
      meta: { requiresAuth: true }
    }
  ],
})

// // Check authentication before each route navigation
// router.beforeEach(async (to, from, next) => {
//   // Initialize auth state if needed
//   if (isAuthenticated.value === undefined) {
//     await initAuth();
//   }
  
//   if (to.meta.requiresAuth && !isAuthenticated.value) {
//     // Redirect to login if trying to access protected route without authentication
//     next('/login');
//   } else if (to.meta.requiresGuest && isAuthenticated.value) {
//     // Redirect to profile if trying to access guest routes when authenticated
//     next('/profile');
//   } else {
//     next();
//   }
// });

export default router;