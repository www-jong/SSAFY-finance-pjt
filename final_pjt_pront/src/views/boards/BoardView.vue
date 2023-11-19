<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-center mb-6">{{route.params.board_type}} 게시판</h1>
    <RouterLink
      :to="{ name: 'CreateView', params: { board_type: route.params.board_type } }"
      class="inline-block bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors"
    >
      [CREATE]
    </RouterLink>
    <ArticleList :board_type="route.params.board_type" :loading="loading" class="mt-4" />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import ArticleList from '@/components/ArticleList.vue'

const route = useRoute()
const store = useCounterStore()
const loading = ref(false) // 로딩 상태 추가

onMounted(async () => {
  loading.value = true // 로딩 시작
  await store.getBoards(route.params.board_type)
  loading.value = false // 로딩 종료
})

watch(() => route.params.board_type, async (newBoardType) => {
  loading.value = true // 로딩 시작
  await store.getBoards(newBoardType)
  loading.value = false // 로딩 종료
});
</script>

<style>

</style>
