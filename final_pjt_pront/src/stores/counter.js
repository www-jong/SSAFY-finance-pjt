import { ref ,computed} from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import {useRouter} from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const token = ref(null)
  const API_URL = import.meta.env.VITE_BACKSERVER
  const router = useRouter()
  const original_username = ref('')
  const isLogin = computed(()=>{
    if (token.value === null){
      return false
    }else{
      return true
    }
  })

  const logIn = function(payload){
    const username = payload.username
    const password = payload.password
    axios({
      method:'post',
      url:`${API_URL}/accounts/login/`,
      data:{
        username,password
      }
    })
    .then(res=>{
      token.value = res.data.key
      original_username.value=username
      router.push({name:'HomeView'})
      console.log('로그인 완료')
    })
    .catch(err => console.log(err))
  }

  const logOut = function(){

      token.value = null
      router.push({name:'HomeView'})
      console.log('로그아웃 완료')
  }

  const signUp = function(payload){
    const username = payload.username
    const password1 = payload.password1
    const password2 = payload.password2

    axios({
      method:'post',
      url:`${API_URL}/accounts/signup/`,
      data:{
        username,password1,password2
      }
    })
    .then(res => {
      console.log('회원가입 완료')
      const password = password1
      logIn({username,password})
    })
    .catch(err => console.log(err))
  }

  const getArticles = function(){
    axios({
      method:'get',
      url:`${API_URL}/boards/articles/`,
      headers:{
        Authorization: `Token ${token.value}`
      }
    })
    .then(res => {
      articles.value = res.data
    })
    .catch(err => console.log(err))
  }
  return {articles, API_URL,original_username, getArticles, signUp, logIn, token,isLogin, logOut}
}, { persist: true })
