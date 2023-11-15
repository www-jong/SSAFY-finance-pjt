<template>
  <div>
    <h5>{{ article.id }}</h5>
    <p>{{ article.title }}</p>
    <p>{{ article.content }}</p>
    <RouterLink :to="{name:'DetailView',params:{id:article.id}}">
    [Detail]
    </RouterLink>
  </div>
  <hr>
</template>

<script setup>
import {RouterLink} from 'vue-router'
defineProps({
  article:Object
})
</script>
