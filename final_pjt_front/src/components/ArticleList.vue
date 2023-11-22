<template>
  <LoadingPage v-if="loading" />
  <div class="mt-6" v-if="filteredArticles.length">
    <div class="space-y-4">
      <ArticleListItem 
      v-for="article in filteredArticles"
      :key="article.id"
      :article="article"
      :board_type="board_type"
      />
    </div>
  </div>
  <div v-else>
    게시글이 없습니다!
  </div>
</template>


<script setup>
import LoadingPage from '@/components/LoadingPage.vue'
import ArticleListItem from '@/components/ArticleListItem.vue'
import { computed, defineProps } from 'vue'
import { useStore } from '@/stores/index'

const props = defineProps({
  board_type: String,
  loading: Boolean // 여기에서 loading을 props로 받습니다.
})

const store = useStore()
const filteredArticles = computed(() => store.articles)
</script>
