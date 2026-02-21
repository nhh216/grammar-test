import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/exam/:sessionId',
      name: 'exam',
      component: () => import('@/views/ExamView.vue'),
      props: (route) => ({ sessionId: Number(route.params.sessionId) }),
    },
    {
      path: '/result/:sessionId',
      name: 'result',
      component: () => import('@/views/ResultView.vue'),
      props: (route) => ({ sessionId: Number(route.params.sessionId) }),
    },
    {
      path: '/topic/:slug',
      name: 'topic',
      component: () => import('@/views/TopicDetailView.vue'),
      props: true,
    },
    {
      path: '/performance',
      name: 'performance',
      component: () => import('@/views/PerformanceView.vue'),
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/HistoryView.vue'),
    },
    {
      path: '/review/:sessionId',
      name: 'review',
      component: () => import('@/views/ReviewView.vue'),
      props: (route) => ({ sessionId: Number(route.params.sessionId) }),
    },
  ],
})

export default router
