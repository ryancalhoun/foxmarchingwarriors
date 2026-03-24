import { createRouter, createWebHistory } from 'vue-router'

import PageContent from '@/components/PageContent'
import UserLogin from '@/components/UserLogin'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: UserLogin,
  },
  {
    path: '/:page',
    name: 'page',
    component: PageContent,
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: { name: 'page', params: { page: 'home' } },
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: routes,
  scrollBehavior(to, from, savedPosition) {
    if(savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  }
})

export default router

