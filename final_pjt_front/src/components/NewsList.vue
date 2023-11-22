<template>
    <div class="max-w-2xl mx-auto py-6">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">오늘의 금융 뉴스</h3>
        <div v-for="news in newsList" :key="news.id" class="mb-2">
            <a :href="news.link" class="text-blue-500 hover:text-blue-700">
                <p v-html="news.title" class="text-lg"></p>
            </a>
        </div>
    </div>
</template>
<script setup>
import { onMounted,onUnmounted,computed } from 'vue'
import { useNewsStore } from '@/stores/news'

const store = useNewsStore()
const intervalId = setInterval(() => {
        store.getNews()
    }, 10000)

onMounted(() => {
    // 초기 뉴스 로드
    store.getNews()

})

onUnmounted(() => {
    // 페이지를 벗어날 때 인터벌 중지
    if (intervalId) {
        clearInterval(intervalId)
    }
})
const newsList = computed(() => store.news)

</script>
<style scoped>

</style>