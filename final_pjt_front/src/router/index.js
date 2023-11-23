import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import KakaoView from '@/views/KakaoView.vue'
import BoardView from '@/views/boards/BoardView.vue'
import DetailView from '@/views/boards/DetailView.vue'
import CreateView from '@/views/boards/CreateView.vue'
import ExChangeView from '@/views/ExChangeView.vue'
import AccountDetailView from '@/views/account/AccountDetailView.vue'
import {useStore} from '@/stores/index'
import FinanceProductView from '@/views/product/FinanceProductView.vue'
import LoginView from '@/views/account/LoginView.vue'
import SignUpView from '@/views/account/SignUpView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView
    },
    {
      path: '/kakao',
      name: 'KakaoView',
      component: KakaoView
    },
    {
      path:'/signup',
      name:'SignUpView',
      component:SignUpView,
      meta: {
        hideNav: true,  // nav 숨김
        hideFoot: true  // foot 숨김
      }
    },
    {
      path:'/login',
      name:'LogInView',
      component:LoginView,
      meta: {
        hideNav: true,  // nav 숨김
        hideFoot: true  // foot 숨김
      }
    },
    {
      path:'/create/:board_type',
      name: 'CreateView',
      component:CreateView
    },
    {
      path:'/Board/:board_type/:article_pk',
      name:'DetailView',
      component:DetailView
    },
    {
      path:'/ExChange',
      name:'ExChangeView',
      component:ExChangeView
    },
    {
      path:'/Board/:board_type',
      name:'BoardView',
      component:BoardView
    },
    {
      path:'/accountinfo/:search_username',
      name:'AccountDetailView',
      component:AccountDetailView
    },
    {
      path:'/FinanceProductView',
      name:'FinanceProductView',
      component:FinanceProductView
    },
  ]
})


router.beforeEach((to, from, next) => {
  const store = useStore()
  if (to.name !== 'LogInView' && to.name !== 'SignUpView' && !store.isLogin) {
    // 로그인이 필요한 페이지에 접근하려고 할 때
    window.alert('로그인이 필요합니다.')
    next({ name: 'LogInView' }) // 로그인 페이지로 리다이렉트
  } else if ((to.name === 'LogInView' || to.name === 'SignUpView') && store.isLogin) {
    // 이미 로그인한 상태에서 로그인 또는 회원가입 페이지에 접근하려고 할 때
    window.alert('이미 로그인되어 있습니다.')
    next({ name: 'HomeView' }) // 홈 페이지 또는 다른 적절한 페이지로 리다이렉트
  } else {
    next() // 다른 경우에는 정상적으로 페이지 이동을 허용
  }
})
export default router

