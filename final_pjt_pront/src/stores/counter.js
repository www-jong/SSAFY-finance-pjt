import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const article = ref([])
  const comments = ref([])
  const token = ref(null)
  const API_URL = import.meta.env.VITE_BACKSERVER
  const router = useRouter()
  const my_id = ref(0)
  const my_email = ref('')
  const my_username = ref('')
  const exchange_data = ref({})
  const exchange_datetime = ref('')
  const my_nickname = ref('')
  const search_user = ref('')
  const deposit_products = ref([])
  const saving_products = ref([])
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const logIn = function (payload) {
    const username = payload.username
    const password = payload.password
    console.log('로그인시도')
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        token.value = res.data.key
        console.log('리턴정보', res.data)
        my_username.value = res.data.username
        my_nickname.value = res.data.nickname
        my_email.value = res.data.email
        my_id.value = res.data.id
        console.log('로그인 정보', res.data, my_nickname)
        router.push({ name: 'HomeView' })
        console.log('로그인 완료')
      })
      .catch(err => console.log('로그인에러', err))
  }

  const logOut = function () {
    token.value = null
    my_username.value = null
    my_nickname.value = null

    router.push({ name: 'HomeView' })
    console.log('로그아웃 완료')
  }

  const signUp = function (payload) {
    const username = payload.username
    const password1 = payload.password1
    const password2 = payload.password2
    const email = payload.email
    const birth = payload.birth // birth 필드 추가
    const gender = payload.gender
    const capital = payload.capital
    const salary = payload.salary
    const nickname = payload.nickname
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, email, birth, gender, capital, salary, nickname
      }
    })
      .then(res => {
        console.log('회원가입 완료')
        const password = password1
        logIn({ username, password })
      })
      .catch(err => console.log(err))
  }

  const getExChange = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/exchange/`,
    })
      .then(res => {
        exchange_data.value = res.data.data
        exchange_datetime.value = res.data.datetime
        console.log(res.data)
      })
      .catch(err => console.log(err))
  }

  const getBoards = function (board_type) {
    console.log('counter-board-type', board_type)
    console.log('token', token.value)
    console.log(articles.value)
    //articles.value=''
    axios({
      method: 'get',
      url: `${API_URL}/boards/${board_type}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        if (res.data.message === 'success') {
          articles.value = res.data.data
        }
        else {
          articles.value = ''
        }
      })
      .catch(err => console.log(err))
  }


  const createArticle = function (payload) {
    console.log('router', payload)
    axios({
      method: 'post',
      url: `${API_URL}/boards/${payload.board_type}/`,
      data: {
        title: payload.title,
        content: payload.content,
        board_type: payload.board_type
      },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        // console.log(res)
        router.push({ name: 'BoardView', params: { board_type: payload.board_type } })
      })
      .catch((err) => {
        console.log(err)
      })
  }
  const DetailArticle = function (payload) {
    console.log('detailarticle', payload)
    axios({
      method: 'get',
      url: `${API_URL}/boards/${payload.board_type}/${payload.article_pk}/`
    })
      .then((res) => {
        // console.log(res.data)
        console.log('data', res.data)
        article.value = res.data.article
        comments.value = res.data.comments
      })
      .catch((err) => {
        console.log(err)
      })
  }


  const createComments = function (payload) {
    console.log('router', payload)
    axios({
      method: 'post',
      url: `${API_URL}/boards/comment/${payload.article_pk}/${payload.parent_pk}/`,
      data: {
        content: payload.content,
      },
      headers: {
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

  const deleteComment = function (payload) {
    return new Promise((resolve, reject) => {
      axios({
        method: 'delete',
        url: `${API_URL}/boards/comment/delete/${payload.article_pk}/${payload.comment_pk}/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      .then(() => {
        alert("댓글이 삭제되었습니다.");
        resolve();
      })
      .catch(err => {
        console.error(err);
        alert("댓글 삭제에 실패했습니다.");
        reject(err);
      });
    });
  };
  
  // store.js
  const get_user_data = function (search_name, errorCallback) {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/profile/get_user_data/${search_name}`,
    })
      .then(res => {
        if (res.data.message === 'success') {
          search_user.value = res.data.data;
        } else {
          alert('없는 사용자입니다.')
          errorCallback();
        }
      })
      .catch(err => {
        alert('없는 사용자입니다.')
        errorCallback();
      });
  };


  const followUser = function (from_user_id, to_user_id) {
    console.log(from_user_id, to_user_id)
    axios({
      method: 'post',
      url: `${API_URL}/accounts/profile/follow/`,
      data: {
        from_user_id: from_user_id,
        to_user_id: to_user_id,
      },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        if (res.data.message === 'followed') {
          alert('팔로우')
          search_user.value.followers.push(my_username.value)
        } else if (res.data.message === 'unfollowed') {
          alert('언팔로우')
          search_user.value.followers = search_user.value.followers.filter(item => item !== my_username.value);
        }
      })
      .catch(err => {
        console.log(err)
      })
  }
  const article_like = function (from_user_id, to_article_id) {
    console.log('article_like', from_user_id, to_article_id)
    axios({
      method: 'post',
      url: `${API_URL}/boards/article/like/`,
      data: {
        from_user_id: from_user_id,
        to_article_id: to_article_id,
      },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        if (res.data.message === 'followed') {
          alert('좋아요')
          article.value.like_users.push(my_username.value)
        } else if (res.data.message === 'unfollowed') {
          alert('좋아요 취소')
          article.value.like_users = article.value.like_users.filter(item => item !== my_username.value);
        }
      })
      .catch(err => {
        console.log(err)
      })
  }

  const aritlce_delete = function (board_type, article_id) {
    axios({
      method: 'delete',
      url: `${API_URL}/boards/${board_type}/`,
      data: {
        article_id: article_id,
      },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => {
        alert("게시글이 삭제되었습니다.");
        router.push({ name: 'BoardView', params: { board_type: board_type } });
      })
      .catch(err => {
        console.error(err);
        alert("게시글 삭제에 실패했습니다.");
      });
  }

  const account_delete = function () {
    axios({
      method: 'delete',
      url: `${API_URL}/accounts/profile/edit/`,
      data: {
        user_id: my_id.value,
      },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => {
        alert("회원탈퇴 완료");
        token.value = null
        my_username.value = null
        my_nickname.value = null

        router.push({ name: 'HomeView' })
      })
      .catch(err => {
        console.error(err);
        alert("탈퇴 에러.");
      });
  }
  const get_deposit_product = function () {
    console.log(token.value)
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/save_deposit_products/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        //alert("예금조회완");
        console.log('예금조회 완')
        console.log(res.data.data)
        deposit_products.value = res.data.data
        //router.push({ name: 'HomeView' })
      })
      .catch(err => {
        console.error(err);
        alert("예금조회 에러.");
      });
  }

  const get_saving_product = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/save_saving_products/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        //alert("예금조회완");
        console.log('적금조회 완')
        saving_products.value = res.data.data
        //router.push({ name: 'HomeView' })
      })
      .catch(err => {
        console.error(err);
        alert("적금조회 에러.");
      });
  }
  return {
    articles,
    article,
    comments,
    API_URL,
    my_id,
    my_username,
    signUp,
    logIn,
    token,
    isLogin,
    logOut,
    getExChange,
    exchange_data,
    exchange_datetime,
    getBoards,
    createArticle, DetailArticle,
    createComments, deleteComment,
    my_nickname,
    get_user_data,
    search_user,
    followUser,
    article_like,
    aritlce_delete,
    account_delete,
    get_deposit_product,
    deposit_products,
    saving_products,
    get_saving_product
  }
}, { persist: true })
