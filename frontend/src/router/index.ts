import { createRouter, createWebHistory } from 'vue-router';
// 1. Import the new component for the default landing page
import LandingView from '../views/LandingView.vue';
// 2. Import HomeView, but it will now be used for the internships route
import HomeView from '../views/HomeView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      // ⭐ Use the new LandingView for the root path
      component: LandingView
    },
    {
      path: '/internships', // ⭐ This is the new path for the internships button
      name: 'internships',
      // ⭐ HomeView (your old landing page) now shows up here
      component: HomeView
    },
    // The original '/about' route (it's often good to keep 'about' if it exists)
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
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
    }
  ]
});

export default router;
