import { createRouter, createWebHistory } from 'vue-router'
import OverviewPage from '../pages/OverviewPage.vue'

const router = createRouter({
  history: createWebHistory('/dashboard/'),
  routes: [
    {
      path: '',
      name: 'overview',
      component: OverviewPage,
    },
  ],
})

export default router
