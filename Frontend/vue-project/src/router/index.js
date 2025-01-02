import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import SignupPage from '../components/SignupPage.vue';
import ChatPage from '../components/ChatPage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupPage,
    },
    {
      path: '/chat',
      name: 'chat',
      meta: { requiresAuth: true },
      component: ChatPage,
    },
  ],
});

router.beforeEach((to, from, next) => {
  console.log('Navigation guard triggered'); // Log this to confirm if the guard is hit
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const isAuthenticated = !!localStorage.getItem('authToken');
  console.log('Requires Auth:', requiresAuth, 'Is Authenticated:', isAuthenticated);

  if (requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next(); // Continue navigation
  }
});


export default router;
