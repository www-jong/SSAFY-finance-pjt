<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-center mb-6">게시글 작성</h1>
    <form @submit.prevent="createArticle" class="max-w-lg mx-auto">
      <input
        type="text"
        v-model.trim="title"
        class="w-full p-2 border border-gray-300 rounded mb-4"
        placeholder="제목을 입력하세요"
      >
      <textarea
        v-model.trim="content"
        class="w-full p-2 border border-gray-300 rounded mb-4"
        placeholder="내용을 입력하세요"
        rows="8"
      ></textarea>
      <input
        type="submit"
        class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        value="작성하기"
      >
    </form>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'
import { useRouter,useRoute } from 'vue-router'

const title = ref(null)
const content = ref(null)
const store = useCounterStore()
const router = useRouter()
const route = useRoute()

const createArticle = function () {
  const payload = {
    title: title.value,
    content: content.value,
    board_type: route.params.board_type,
  };
  store.createArticle(payload)
}



</script>

<style>

</style>
