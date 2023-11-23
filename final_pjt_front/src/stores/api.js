import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useApiStore = defineStore('news', () => {
    const NASDAQ_API_KEY = import.meta.env.VITE_NASDAQ
    const golds=ref('')
    const silvers=ref('')
    const URL = 'http://127.0.0.1:8000'
    const getGold = function () {
        axios({
            method: 'GET',
            url: `${URL}/api/v1/golds`
        })
            .then(res => {
                console.log('금데이터',res.data)
                golds.value=res.data.data
            })
            .catch(err => console.log(err))
    }
    const getSilver = function () {
        axios({
            method: 'GET',
            url: `${URL}/api/v1/silvers`
        })
            .then(res => {
                console.log('실버데이터',res.data)
                silvers.value=res.data.data
            })
            .catch(err => console.log(err))
    }


    const news = ref([])
    const getNews = function () {
        axios({
            method: 'GET',
            url: `${URL}/api/v1/news`
        })
            .then(res => {
                console.log(res.data)
                news.value = res.data.items
            })
            .catch(err => console.log(err))
    }
    return { getGold,getNews,news,golds,silvers,getSilver }
}, { persist: true })