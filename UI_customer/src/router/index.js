import { createRouter, createWebHistory } from 'vue-router';
import HorizonView from '@/views/HorizonView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'horizon',
      component: HorizonView,
    },
  ],
});

export default router;
