<script setup>
import { onMounted } from 'vue'
import { useNewsStore } from '../stores/news'

const store = useNewsStore()

onMounted(() => {
    store.getNews()
})

const newsList = store.news

</script>

<template>
    <div>
        <h3>오늘의 금융 뉴스</h3>
            <p v-for="news in newsList">
                <a :href="news.link"><p v-html="news.title"></p></a>
            </p>
    </div>
</template>

<style scoped>

</style>