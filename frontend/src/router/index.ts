// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/LandingView.vue')
    },
    {
      path: '/internships',
      name: 'internships',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/networking',
      name: 'networking',
      component: () => import('../views/NetworkingView.vue')
    },
    {
      path: '/team',
      name: 'team',
      component: () => import('../views/TeamView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/join',
      name: 'join',
      component: () => import('../views/JoinView.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue')
    },
    {
      path: '/edit-profile',
      name: 'edit-profile',
      component: () => import('../views/EditProfileView.vue')
    },
    {
      path: '/saved-listings',
      name: 'saved-listings',
      component: () => import('../views/SavedListingsView.vue')
    }
  ]
});

export default router;
