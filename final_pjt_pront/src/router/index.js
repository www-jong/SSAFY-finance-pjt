import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import KakaoView from '@/views/KakaoView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import BoardView from '@/views/boards/BoardView.vue'
import DetailView from '@/views/boards/DetailView.vue'
import CreateView from '@/views/boards/CreateView.vue'
import ExChangeView from '@/views/ExChangeView.vue'
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

