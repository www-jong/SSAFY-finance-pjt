<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-center mb-6">{{route.params.board_type}} 게시판</h1>
    <RouterLink
      :to="{ name: 'CreateView', params: { board_type: route.params.board_type } }"
      class="inline-block bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors"
    >
      [CREATE]
    </RouterLink>
    <ArticleList :board_type="route.params.board_type" class="mt-4" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import ArticleList from '@/components/ArticleList.vue'
import { watch } from 'vue';

const route = useRoute()
const store = useCounterStore()
console.log('views-board-type',route.params.board_type)
onMounted(() => {
  console.log('dd')
  store.getBoards(route.params.board_type)
})

watch(() => route.params.board_type, (newBoardType, oldBoardType) => {
  console.log('watch',newBoardType, oldBoardType)
    store.getBoards(newBoardType)
});
</script>

<style>

</style>
