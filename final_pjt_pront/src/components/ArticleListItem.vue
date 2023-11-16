<template>
  <div class="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-shadow">
    <h5 class="text-sm font-semibold text-gray-700">작성자 : {{ article.user.username }} 별명 : {{ article.user.nickname }}</h5>
    <p class="text-lg font-bold text-gray-900">제목 : {{ article.title }}</p>
    <p class="text-gray-600">내용 : {{ article.content }}</p>
    <RouterLink
      :to="{name:'DetailView', params:{board_type:board_type,article_pk:article.id}}"
      class="mt-3 inline-block bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors"
    >
      [Detail]
    </RouterLink>
  </div>
  <hr class="my-4">
</template>


<script setup>
import {RouterLink} from 'vue-router'
defineProps({
  article:Object,
  board_type:String
})
</script>
