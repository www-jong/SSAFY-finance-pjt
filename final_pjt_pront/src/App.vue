<template>
  <header>
    <nav>
      <RouterLink :to="{name:'HomeView'}">Home</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>

<script setup>
import { RouterView,RouterLink } from 'vue-router'
</script>

<style scoped>
</style>
