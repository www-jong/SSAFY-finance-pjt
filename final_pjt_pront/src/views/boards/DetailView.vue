<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold text-center mb-6">Detail</h1>
    <!-- 뒤로 가기 버튼 -->
    <button 
      @click="goBack" 
      class="mb-6 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      뒤로 가기
    </button>
    <div v-if="article && article.user" class="bg-white p-4 rounded-lg shadow-md">
      <p class="text-md text-gray-700"><span class="font-semibold">작성자:</span> {{article.user.username }} <span class="font-semibold">별명:</span> {{ article.user.nickname }}</p>
      <p class="text-lg font-bold text-gray-900 mt-2">제목: {{ article.title }}</p>
      <p class="text-gray-600 mt-2">내용: {{ article.content }}</p>
      <p class="text-sm text-gray-500 mt-2">작성일: {{ article.created_at }}</p>
      <p class="text-sm text-gray-500 mt-2">수정일: {{ article.updated_at }}</p>
      <div class="mt-6">
        <h2 class="text-xl font-bold mb-3">댓글 작성하기</h2>
        <textarea v-model.trim="newComment" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="댓글을 입력하세요"></textarea>
        <button @click="submitComment(0)" class="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">댓글 작성</button>
      </div>
      <div class="mt-6">
        <h2 class="text-xl font-bold mb-3">댓글 목록</h2>
        <div class="space-y-4">
          <div 
            v-for="comment in filteredComments" 
            :key="comment.id" 
            class="bg-gray-100 p-3 rounded-lg"
          >

            <p class="font-semibold">{{ comment.user.username }} ({{ comment.user.nickname }})</p>
            <p>{{ comment.content }}</p>
            <p class="text-sm text-gray-600">{{ formatDate(comment.created_at) }}</p>

            <!-- 대댓글 작성 버튼 -->
            <button @click="toggleReplyForm(comment.id)" class="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              대댓글 작성
            </button>

            <!-- 대댓글 작성 영역 -->
            <div v-if="comment.showReplyForm" class="mt-2">
              <textarea v-model.trim="comment.newReply" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="대댓글을 입력하세요"></textarea>
              <button @click="submitReply(comment.id)" class="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                대댓글 작성
              </button>
            </div>

            <!-- 대댓글 표시 -->
            <div class="space-y-2">
              <div 
                v-for="reply in filteredReply.filter(c => c.parent_comment === comment.id)" 
                :key="reply.id" 
                class="bg-gray-200 p-2 rounded-lg ml-4"
              >
                <p class="font-semibold">{{ reply.user.username }} ({{ reply.user.nickname }})</p>
                <p>{{ reply.content }}</p>
                <p class="text-sm text-gray-600">{{ formatDate(reply.created_at) }}</p>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
    <div v-else>
      로딩중입니다..
    </div>
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
  const payload={
    board_type:route.params.board_type,
    article_pk:route.params.article_pk
  }
  store.DetailArticle(payload)
  console.log('로드',article.value)
  console.log('로드 댓글',comments.value)
})
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
  console.log('댓글작성! 추가전 댓글들',comments.value)
  console.log('닉네넴',store.original_nickname)
  const newCommentObject = {
    article_pk: route.params.article_pk,
    content: newComment.value,
    parent_pk:parent_pk,
    parent_comment: parent_pk === 0 ? null : parent_pk,
    user:{username:store.original_username,nickname:store.original_nickname},
    created_at:'now',
    id:'임시요'

  };

  store.createComments({
    article_pk: route.params.article_pk,
    content: newComment.value,
    parent_pk:parent_pk
  })
  comments.value.push(newCommentObject)
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
    user: { username: store.original_username, nickname: store.original_nickname },
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
const goBack = () => {
  router.back()
}

</script>

<style>

</style>
