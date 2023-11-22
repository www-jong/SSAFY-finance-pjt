<template>
  <main class="bg-gray-100 min-h-screen p-8">
    <h1 class="text-xl font-bold text-gray-700 mb-4">주변 은행 검색</h1>
    <KaKaoMap/>
    <NavBar/>
  </main>
</template>

<script setup>
import KaKaoMap from '@/components/KakaoMap.vue'
import NavBar from '@/components/NavBar.vue'
</script>
