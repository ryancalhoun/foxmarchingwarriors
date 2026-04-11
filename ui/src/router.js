import { createRouter, createWebHistory } from 'vue-router'

import PageContent from '@/components/PageContent'
import UserLogin from '@/components/UserLogin'
import UserProfile from '@/components/UserProfile'
import SiteSettings from '@/components/SiteSettings'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: UserLogin,
  },
  {
    path: '/change-password',
    name: 'change',
    component: UserLogin,
  },
  {
    path: '/forgot-password',
    name: 'forgot',
    component: UserLogin,
  },
  {
    path: '/reset-password',
    name: 'reset',
    component: UserLogin,
  },
  {
    path: '/user',
    name: 'user',
    component: UserProfile,
  },
  {
    path: '/settings',
    name: 'settings',
    component: SiteSettings,
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
  history: createWebHistory('/'),
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

