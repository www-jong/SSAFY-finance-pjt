import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import KakaoView from '@/views/KakaoView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ArticleView from '@/views/ArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'

import {useCounterStore} from '@/stores/counter'
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
      component:SignUpView
    },
    {
      path:'/login',
      name:'LogInView',
      component:LogInView
    },
    {
      path:'/create',
      name: 'CreateView',
      component:CreateView
    },
    {
      path: '/article',
      name: 'ArticleView',
      component:ArticleView
    },
    {
      path:'/articles/:id',
      name:'DetailView',
      component:DetailView
    },
  ]
})

router.beforeEach((to,from)=>{
  const store=useCounterStore()
  if(to.name==='ArticleView'&& !store.isLogin){
    window.alert('로그인이 필요합니다.')
    return{name:'LogInView'}
  }
  if((to.name==='SignUpView'||to.name==='LogInView')&&(store.isLogin)){
    window.alert('이미 로그인이 되어있습니다.')
    return{name:'ArticleView'}
  }
})
export default router

