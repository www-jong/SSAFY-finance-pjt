<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold text-center mb-6">Detail</h1>
    
    <!-- 뒤로 가기 버튼 -->
    <button @click="goBack" class="mb-6 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">뒤로 가기</button>

    <hr>
    <div v-if="article && article.user" class="bg-white p-4 rounded-lg shadow-md">
      <p class="text-sm text-gray-700 text-right"><span class="font-semibold">작성자:</span> {{ article.user.username }} <span class="font-semibold">별명:</span> {{ article.user.nickname }}</p>
      <p class="text-2xl font-bold text-gray-900 mt-2">제목: {{ article.title }}</p>
      <hr>
      <p class="text-lg text-gray-600 mt-2">내용: {{ article.content }}</p>
      <br>
      <br>
      <hr>
      <p class="text-xs text-gray-500 mt-2 text-right">작성일: {{ formatDate(article.created_at) }}</p>
      <p class="text-xs text-gray-500 mt-2 text-right">수정일: {{ formatDate(article.updated_at) }}</p>

      <div>
        <!-- 좋아요 버튼 -->
        <button @click="toggleArticleLike" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          좋아요 {{ article.like_users.length }}
        </button>
        <!-- 게시글 삭제 버튼 -->
        <button v-if="isArticleOwner" @click="deleteArticle" class="mt-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded" style="float: right">게시글 삭제</button>
        <!-- 게시글 수정 버튼 -->
        <button v-if="isArticleOwner" @click="editArticle" class="mt-4 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded" style="float: right">게시글 수정</button>
      </div>

      <!-- 게시글 수정 폼 -->
      <div v-if="editArticleMode" class="mt-4">
        <input v-model="editArticleTitle" type="text" class="w-full p-2 border rounded mb-2">
        <textarea v-model="editArticleContent" class="w-full p-2 border rounded" style="height: 300px"></textarea>
        <div class="text-right">
          <button @click="updateArticle" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">저장</button>
        </div>
      </div>

      <br>
      <hr>

      <!-- 댓글 작성 폼 -->
      <div class="mt-6">
        <h2 class="text-xl font-bold mb-3">댓글 작성하기</h2>
        <textarea v-model.trim="newComment" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="댓글을 입력하세요"></textarea>
        <div class="text-right">
          <button @click="submitComment(0)" class="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">댓글 작성</button>
        </div>
      </div>

      <br>
      <hr>

      <!-- 댓글 목록 -->
      <div class="mt-6">
        <h2 class="text-xl font-bold mb-3">댓글 목록</h2>
        <div class="space-y-4">
          <div v-for="comment in filteredComments" :key="comment.id" class="bg-gray-100 p-3 rounded-lg">
            <!-- 댓글 수정 영역 -->
            <div v-if="comment.editMode" class="mt-2">
              <textarea v-model="comment.editContent" class="w-full p-2 border rounded"></textarea>
              <button @click="saveEdit(comment)" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">저장</button>
            </div>

            <p class="font-semibold">{{ comment.user.username }} ({{ comment.user.nickname }})</p>
            <p>{{ comment.content }}</p>            
            <p class="text-sm text-gray-600">{{ formatDate(comment.created_at) }}</p>


            <div>
        <button @click="toggleReplyForm(comment.id)" class="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          답글 작성
        </button>
        <button v-if="isCommentOwner(comment)" @click="deleteComment(comment)" class="mt-2 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded" style="float: right">댓글 삭제</button>
      
        <button v-if="isCommentOwner(comment)" @click="editComment(comment)" class="mt-2 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded" style="float: right">댓글 수정</button>
      </div>

            <!-- 대댓글 작성 영역 -->            
            <div v-if="comment.showReplyForm" class="mt-2 text-right">
              <textarea v-model.trim="comment.newReply" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="답글을 입력하세요"></textarea>
              <button @click="submitReply(comment.id)" class="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">등록</button>
            </div>

            <!-- 대댓글 목록 -->
            <div class="mt-2 space-y-2">
              <div v-for="reply in filteredReply.filter(c => c.parent_comment === comment.id)" :key="reply.id" class="bg-gray-200 p-2 rounded-lg ml-4">
                <p class="font-semibold">{{ reply.user.username }} ({{ reply.user.nickname }})</p>
                <p>{{ reply.content }}</p>
                <p class="text-sm text-gray-600">{{ formatDate(reply.created_at) }}</p>
                <div class="text-right">
      <button v-if="isCommentOwner(reply)" @click="deleteComment(reply)" class="mt-2 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">댓글 삭제</button>
    </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>로딩중입니다..</div>
  </div>
</template>




<script setup>
import axios from 'axios'
import { onMounted,onBeforeMount, ref,computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import router from '../../router';

const store = useCounterStore()
const route = useRoute()

const newComment = ref('')
const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  const seconds = date.getSeconds().toString().padStart(2, '0');

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};


onMounted(() => {
  const payload = {
    board_type: route.params.board_type,
    article_pk: route.params.article_pk
  };
  store.DetailArticle(payload);
});
const article= computed(() => store.article)
const comments = computed(() => store.comments)
const filteredComments = computed(() => {
  return comments.value.filter(comment => comment.parent_comment === null);
});
const filteredReply = computed(() => {
  return comments.value.filter(comment => comment.parent_comment != null);
});

const submitComment = (parent_pk) => {
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력해주세요.');
    return;
  }
  const maxId = comments.value.reduce((max, comment) => Math.max(max, comment.id), 0);
  const newCommentObject = {
    article_pk: route.params.article_pk,
    content: newComment.value,
    parent_pk:parent_pk,
    parent_comment: parent_pk === 0 ? null : parent_pk,
    user:{username:store.my_username,nickname:store.my_nickname},
    created_at:'now',
    id:maxId+1

  };
  store.createComments({
    article_pk: route.params.article_pk,
    content: newComment.value,
    parent_pk:parent_pk
  })
  comments.value.push(newCommentObject)
  router.go(0)
  newComment.value=''
}



const toggleReplyForm = (commentId) => {
  const comment = comments.value.find((c) => c.id === commentId);
  if (comment) {
    comment.showReplyForm = !comment.showReplyForm;
  }
};

const submitReply = (commentId) => {
  const comment = comments.value.find((c) => c.id === commentId);
  if (!comment.newReply.trim()) {
    alert('대댓글 내용을 입력해주세요.');
    return;
  }

  const newCommentObject = {
    article_pk: route.params.article_pk,
    content: comment.newReply,
    parent_comment: commentId === 0 ? null : commentId,
    user: { username: store.my_username, nickname: store.my_nickname },
    created_at: new Date().toISOString(),
    id: '임시요' // 실제로는 고유한 ID를 생성해야 합니다.
  };

  store.createComments({
    article_pk: route.params.article_pk,
    content: comment.newReply,
    parent_pk: commentId
  });

  comments.value.push(newCommentObject); // 대댓글을 comments 배열에 추가
  comment.newReply = '';
  comment.showReplyForm = false; // 대댓글 작성 영역 닫기
};
const toggleArticleLike = (article) => {
  store.article_like(store.my_id,route.params.article_pk)
  // 서버에 게시글 좋아요 상태를 토글하는 요청 보내기
  // 예: axios.post(...)
  // 응답에 따라 article.like_users 및 article.isLikedByCurrentUser 업데이트
};

const toggleCommentLike = (comment) => {
  // 서버에 댓글 좋아요 상태를 토글하는 요청 보내기
  // 예: axios.post(...)
  // 응답에 따라 comment.like_users 및 comment.isLikedByCurrentUser 업데이트
};

// 게시글 수정

const editArticleMode = ref(false);
const editArticleTitle = ref("");
const editArticleContent = ref("");

const updateArticle = () => {
  if (!editArticleTitle.value.trim() || !editArticleContent.value.trim()) {
    alert('게시글의 제목과 내용을 입력해주세요.');
    return;
  }

  store.updateArticle({
    board_type: route.params.board_type,
    article_pk: route.params.article_pk,
    title: editArticleTitle.value,
    content: editArticleContent.value
  }).then(() => {
    // 수정 성공 시 처리
    alert("게시글이 성공적으로 수정되었습니다.");

    // 수정 모드 종료
    editArticleMode.value = false;

    // 수정된 게시글의 제목과 내용을 로컬 상태에 반영
    article.value.title = editArticleTitle.value;
    article.value.content = editArticleContent.value;

    // 선택적: 게시글 상세 페이지로 리디렉션하거나 페이지 새로고침
    // router.push({ name: 'ArticleDetail', params: { board_type: route.params.board_type, article_pk: route.params.article_pk } });
    // 또는
    // window.location.reload();
  }).catch(err => {
    console.error("게시글 수정 실패:", err);
    alert("게시글 수정에 실패했습니다.");
  });
};

const editArticle = () => {
  editArticleMode.value = true;
  editArticleTitle.value = article.value.title;
  editArticleContent.value = article.value.content;
};

// 댓글 수정
const editComment = (comment) => {
  comment.editMode = true;
  comment.editContent = comment.content;
};

const saveEdit = (comment) => {
  if (comment.editContent && comment.editContent !== comment.content) {
    store.updateComment({
      article_pk: article.value.id,
      comment_pk: comment.id,
      content: comment.editContent
    }).then(() => {
      comment.content = comment.editContent;
      comment.editMode = false;
    }).catch(err => {
      console.error("댓글 수정 실패:", err);
      alert("댓글 수정에 실패했습니다.");
    });
  }
};

// 게시글 삭제
const deleteArticle = () => {
  if (confirm("게시글을 삭제하시겠습니까?")) {
    console.log("게시글 삭제 작업 시작");
    store.article_delete(route.params.board_type, article.value.id) // 여기 수정
    .then(() => {
      console.log("게시글 삭제 성공");
      router.push({ name: 'BoardView', params: { board_type: route.params.board_type } });
    })
    .catch(err => {
      console.error("게시글 삭제 실패:", err);
    });
  } else {
    console.log("게시글 삭제 작업 취소");
  }
};

// 댓글 삭제
const deleteComment = (comment) => {
  if (confirm("댓글을 삭제하시겠습니까?")) {
    const payload = {
      article_pk: article.value.id, // 현재 게시글의 ID
      comment_pk: comment.id       // 삭제할 댓글의 ID
    };

    store.deleteComment(payload)
      .then(() => {
        // 성공적으로 삭제된 댓글을 목록에서 제거
        comments.value = comments.value.filter(c => c.id !== comment.id);
        router.go(0)
      })
      .catch(err => {
        console.error("댓글 삭제 실패:", err);
      });
  }
};

// 뒤로 가기
const goBack = () => {
  router.back(route.params.article_pk);
};

// 게시글 작성자 확인
const isArticleOwner = computed(() => {
  return article.value && store.my_username === article.value.user.username;
});

// 댓글 작성자 확인
const isCommentOwner = (comment) => {
  return comment.user.username === store.my_username;
};
</script>

<style>

</style>