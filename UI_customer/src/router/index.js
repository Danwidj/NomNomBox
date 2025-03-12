import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Cart from '../views/Cart.vue'
import Product from '../views/Product.vue'
import Profile from '../views/Profile.vue'
import Chatbot from '../views/Chatbot.vue'
import EditProfile from '../views/EditProfile.vue'

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
    },
    {
      path: '/edit-profile',
      name: 'edit-profile',
      component: EditProfile,
    }
    
  ],
})

export default router
