<template>

        <h3 class="text-xl font-semibold text-gray-500 mb-4">오늘의 금융 뉴스</h3>
        <div v-for="news in newsList" :key="news.id" class=" p-4 rounded-lg shadow bg-white hover:shadow-md transition-shadow">
            <a :href="news.link" class="text-blue-500 hover:text-blue-700">
                <p v-html="news.title" class="text-lg"></p>
            </a>
        </div>
</template>
<script setup>
import { onMounted,onUnmounted,computed } from 'vue'
import { useApiStore } from '@/stores/api'

const apistore = useApiStore()
const intervalId = setInterval(() => {
    apistore.getNews()
    }, 10000)

onMounted(() => {
    // 초기 뉴스 로드
    apistore.getNews()

})

onUnmounted(() => {
    // 페이지를 벗어날 때 인터벌 중지
    if (intervalId) {
        clearInterval(intervalId)
    }
})
const newsList = computed(() => apistore.news)

</script>
<style scoped>

</style>