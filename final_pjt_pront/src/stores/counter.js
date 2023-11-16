import { ref ,computed} from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import {useRouter} from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const article = ref([])
  const comments = ref([])
  const token = ref(null)
  const API_URL = import.meta.env.VITE_BACKSERVER
  const router = useRouter()
  const original_username = ref('')
  const exchange_data=ref({})
  const exchange_datetime=ref('')

  console.log('@@@',articles)
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
    const birth =  payload.birth // birth 필드 추가
    const gender = payload.gender
    const capital = payload.capital
    const salary = payload.salary
    const nickname = payload.nickname
    axios({
      method:'post',
      url:`${API_URL}/accounts/signup/`,
      data:{
        username,password1,password2,birth,gender,capital,salary,nickname
      }
    })
    .then(res => {
      console.log('회원가입 완료')
      const password = password1
      logIn({username,password})
    })
    .catch(err => console.log(err))
  }

  const getExChange = function(){
    axios({
      method:'get',
      url:`${API_URL}/api/v1/exchange/`,
    })
    .then(res => {
      exchange_data.value=res.data.data
      exchange_datetime.value=res.data.datetime
      console.log(res.data)
    })
    .catch(err => console.log(err))
  }

  const getBoards = function(board_type){
    console.log('counter-board-type',board_type)
    console.log('token',token.value)
    console.log(articles.value)
    //articles.value=''
    axios({
      method:'get',
      url:`${API_URL}/boards/${board_type}/`,
      headers:{
        Authorization: `Token ${token.value}`
      }
    })
    .then(res => {
      articles.value = res.data
    })
    .catch(err => console.log(err))
  }


  const createArticle = function (payload) {
    console.log('router',payload)
    axios({
      method: 'post',
      url: `${API_URL}/boards/${payload.board_type}/`,
      data: {
        title: payload.title,
        content: payload.content,
        board_type:payload.board_type
      },
      headers:{
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        // console.log(res)
        router.push({ name: 'BoardView',params: { board_type: payload.board_type }})
      })
      .catch((err) => {
        console.log(err)
      })
  }
  const DetailArticle = function (payload) {
    console.log('detailarticle',payload)
    axios({
      method: 'get',
      url: `${API_URL}/boards/${payload.board_type}/${payload.article_pk}/`
    })
      .then((res) => {
        // console.log(res.data)
        console.log('data',res.data)
        article.value = res.data.article
        comments.value=res.data.comments
      })
      .catch((err) => {
        console.log(err)
      })
  }


  const createComments = function (payload) {
    console.log('router',payload)
    axios({
      method: 'post',
      url: `${API_URL}/boards/comment/${payload.article_pk}/${payload.parent_pk}/`,
      data: {
        content: payload.content,
      },
      headers:{
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        // console.log(res)
        console.log(res.data.message)
      })
      .catch((err) => {
        console.log(err)
      })
  }
  return {articles,article,comments, API_URL,original_username, signUp, logIn, token,isLogin, logOut,getExChange,exchange_data,exchange_datetime,getBoards,createArticle,DetailArticle,createComments}
}, { persist: true })
