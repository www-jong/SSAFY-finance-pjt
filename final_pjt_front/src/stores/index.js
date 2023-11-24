import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useStore = defineStore('counter', () => {
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
  const search_user_articles= ref('')
  const search_user_comments= ref('')
  const join_deposit_products=ref('')
  const search_user_products = ref('')
  const join_saving_products=ref('')
  const account_edit_check=ref(false)
  const loading=ref(false)
  const account_image_modal_status=ref(false)
  const account_modal_status=ref(false)
  const deposit_products = ref([])
  const saving_products = ref([])
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const parseErrorMessages = (errorResponse) => {
    let messages = [];
    console.log('에러출력',errorResponse)
    const data = JSON.parse(errorResponse);
    if (data && typeof data === 'object') {
      // 각 필드에 대한 에러 메시지를 배열에 추가합니다.
      Object.keys(data).forEach(key => {
        messages = messages.concat(data[key]);
      });
    }
    return messages.join('\n');
  };


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
      .catch(err => {
      const errorMessages = parseErrorMessages(err.request.response);
      alert(errorMessages)
    })
  }

  const logOut = function () {
    token.value = null;
    my_username.value = null;
    my_nickname.value = null;
  
    console.log('로그아웃 완료');
  }

  const signUp = function (payload) {
    const username = payload.username
    const password1 = payload.password1
    const password2 = payload.password2
    const email = payload.email
    const birth = payload.birth // birth 필드 추가
    const age = payload.age
    const gender = payload.gender
    const capital = payload.capital
    const salary = payload.salary
    const nickname = payload.nickname
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, age,email, birth, gender, capital, salary, nickname
      }
    })
      .then(res => {
        console.log('회원가입 완료')
        const password = password1
        logIn({ username, password })
      })
      .catch(err => {
        const errorMessages = parseErrorMessages(err.request.response);
        alert(errorMessages);
      });
  }

  const account_edit = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/profile/edit/`,
      data:payload,
      headers: {
        Authorization: `Token ${token.value}`
      }
      
    })
      .then(res => {
        if(res.data.message==='success'){
          account_modal_status.value=false
        console.log('수정 완료')
        alert('수정이 완료되었습니다.\n 다시 로그인해주세요.')
        logOut()
      }
      else{
        alert(res.data)
      }
      })
      .catch((err) => {
        console.log(err)
        alert(err.response.data.data)
      });
  }

  const account_image_edit = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/profile/image_edit/`,
      data:payload,
      headers: {
        Authorization: `Token ${token.value}`
      }
      
    })
      .then(res => {
        if(res.data.message==='success'){
          search_user.value.image = res.data.data;
        console.log('수정 완료',res.data.data)
        alert('수정이 완료되었습니다.',res.data.data)
        account_image_modal_status.value=false
      }
      else{
        alert(res.data)
      }
      })
      .catch((err) => {
        console.log(err)
        alert(err.response.data.data)
      });
  }

  const getExChange = function () {
    loading.value=true
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/exchange/`,
    })
      .then(res => {
        exchange_data.value = res.data.data
        exchange_datetime.value = res.data.datetime
        console.log(res.data)
        loading.value=false
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

  const updateArticle = function (payload) {
    console.log(payload)
    return axios({
      method: 'put',
      url: `${API_URL}/boards/${payload.board_type}/${payload.article_pk}/update/`,
      data: {
        title: payload.title,
        content: payload.content,
        board_type:payload.board_type
      },
      headers: {
        Authorization: `Token ${token.value}`,
      }
    })
    .then(response => {
      // 서버 응답으로 게시글 데이터 업데이트
      if (response.data && article.value.id === payload.article_pk) {
        article.value.title = response.data.title;
        article.value.content = response.data.content;
        // 여기서 필요한 다른 게시글 정보도 업데이트 가능
      }
    })
    .catch(err => {
      console.error("게시글 수정 실패:", err);
    });
  };

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

  const updateComment = function (payload) {
    return axios({
      method: 'put',
      url: `${API_URL}/boards/comment/${payload.article_pk}/${payload.comment_pk}/update/`,
      data: { content: payload.content },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(response => {
      // 서버 응답으로 댓글 데이터 업데이트
      const updatedIndex = comments.value.findIndex(c => c.id === payload.comment_pk);
      if (updatedIndex !== -1) {
        comments.value[updatedIndex].content = response.data.content; // 댓글 내용 업데이트
      }
    })
    .catch(err => {
      console.error("댓글 수정 실패:", err);
    });
  };

  const deleteComment = function (payload) {
    return new Promise((resolve, reject) => {
      axios({
        method: 'delete',
        url: `${API_URL}/boards/comment/${payload.article_pk}/${payload.comment_pk}/delete/`,
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
          console.log(res.data)
          search_user.value = res.data.user_data;
          search_user_comments.value=res.data.user_comments
          search_user_articles.value=res.data.user_articles
          search_user_products.value=res.data.user_products
        
        } else {
          alert('없는 사용자입니다.2')
          errorCallback();
        }
      })
      .catch(err => {
        alert('없는 사용자입니다.3',err)
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

  const article_delete = function (board_type, article_id) {
    axios({
      method: 'delete',
      url: `${API_URL}/boards/${board_type}/${article_id}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(() => {
      alert("게시글이 삭제되었습니다.");
      router.push({ name: 'BoardView', params: { board_type } });
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
    loading.value=true
    console.log(token.value)
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/save_deposit_products/`,
    })
      .then(res => {
        //alert("예금조회완");
        console.log('예금조회 완료')
        loading.value=false
        deposit_products.value = res.data.data
      })
      .catch(err => {
        console.error(err);
        alert("예금조회 에러.");
      });
  }

  const get_saving_product = function () {
    loading.value=true
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/save_saving_products/`,
    })
      .then(res => {
        //alert("예금조회완");
        console.log('적금조회 완료')
        loading.value=false
        saving_products.value = res.data.data
      })
      .catch(err => {
        console.error(err);
        alert("적금조회 에러.");
      });
  }
  const join_product = function (type,code) {
    loading.value=true
    console.log('@@@@@@',type)
    axios({
      method: 'post',
      url: `${API_URL}/api/v1/join_${type}_product/`,
      data: {
        code: code,
      },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        //alert("예금조회완");
        loading.value=false
        if (type === 'deposit') {
          const index = deposit_products.value.findIndex(product => product.code === code);
          console.log('dd')
          if (index !== -1) {
            deposit_products.value[index] = res.data.data;
            console.log('찾음')
          }
        } else {
          const index = saving_products.value.findIndex(product => product.code === code);
          if (index !== -1) {
            saving_products.value[index] = res.data.data;
          }
        }
        console.log('가입 완')
        loading.value=false
        alert(res.data.message)
        
      })
      .catch(err => {
        console.error(err);
        alert("예금가입 에러.");
      });
  }

  return {
    account_image_edit,
    account_edit_check,
    account_edit,
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
    createArticle, DetailArticle, updateArticle,
    createComments, updateComment, deleteComment,
    my_nickname,
    get_user_data,
    search_user,
    followUser,
    article_like,
    article_delete,
    account_delete,
    get_deposit_product,
    deposit_products,
    saving_products,
    get_saving_product,
    search_user_comments,
    search_user_articles,
    join_product,
    loading,
    search_user_products,
    account_modal_status,
    account_image_modal_status,
    
  }
}, { persist: true })