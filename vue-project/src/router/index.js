import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../components/LoginView.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import LijecnikDashboard from '../components/LijecnikDashboard.vue'
import MedDjelatnikDashboard from '../components/MedDjelatnikDashboard.vue'
import listaPacijenata from '../components/listaPacijenata.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'administrator' }
  },
  {
    path: '/lijecnik',
    name: 'LijecnikDashboard',
    component: LijecnikDashboard,
    meta: { requiresAuth: true, role: 'lijecnik' }
  },
  {
    path: '/medicinski-djelatnik',
    name: 'MedDjelatnikDashboard',
    component: MedDjelatnikDashboard,
    meta: { requiresAuth: true, role: 'medicinski_djelatnik' }
  },
  {
    path: '/patients',
    name: 'listaPacijenata',
    component: listaPacijenata,
    meta: { requiresAuth: true, allowedRoles: ['administrator', 'lijecnik', 'medicinski_djelatnik'] }
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user'))

  if (to.meta.requiresAuth) {
    if (!user) {
      return next('/login')
    }

    // Handle single role OR multiple allowed roles
    if (to.meta.role && user.role !== to.meta.role) {
      return next('/login')
    }

    if (to.meta.allowedRoles && !to.meta.allowedRoles.includes(user.role)) {
      return next('/login')
    }

    return next()
  }

  next()
})

export default router
