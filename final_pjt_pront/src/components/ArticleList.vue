<template>
  <div>
    <h3>Article List</h3>
    <ArticleListItem 
    v-for="article in store.articles"
    :key="article.id"
    :article="article"
    />
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue'
import {useCounterStore} from '@/stores/counter'
const store=useCounterStore()
</script>
