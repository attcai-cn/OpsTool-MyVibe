import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('@/views/DashboardView.vue'),
    },
    {
      path: '/notes',
      name: 'Notes',
      component: () => import('@/views/NotesView.vue'),
    },
    {
      path: '/notes/:id',
      name: 'NoteDetail',
      component: () => import('@/views/NoteDetailView.vue'),
    },
    {
      path: '/cheatsheet',
      name: 'Cheatsheet',
      component: () => import('@/views/CheatsheetView.vue'),
    },
    {
      path: '/calculator',
      name: 'Calculator',
      component: () => import('@/views/CalculatorView.vue'),
    },
    {
      path: '/cron',
      name: 'Cron',
      component: () => import('@/views/CronView.vue'),
    },
    {
      path: '/todos',
      name: 'Todos',
      component: () => import('@/views/TodoView.vue'),
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (!to.meta.public && !authStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
