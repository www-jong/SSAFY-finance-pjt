<template>
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
    게시글을 불러오는 중입니다...
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue'
import { computed } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const { board_type } = defineProps({ board_type: String })

const filteredArticles = computed(() => store.articles)
</script>
