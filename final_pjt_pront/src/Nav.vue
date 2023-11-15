<template>
  <header>
    <nav>
      <RouterLink :to="{name:'ArticleView'}">Articles</RouterLink>
      <RouterLink :to="{name:'SignUpView'}">SignUpPage</RouterLink>
      <RouterLink :to="{name:'LogInView'}">LogInPage</RouterLink>
    </nav>
  </header>
</template>

<script setup>
import { RouterView,RouterLink } from 'vue-router'
</script>

<style scoped>
</style>
