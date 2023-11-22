import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useNewsStore = defineStore('news', () => {
  const news = ref([])
  const URL = 'http://127.0.0.1:8000'
  const getNews = function() {
    axios({
      method: 'GET',
      url: `${URL}/api/v1/news`
    })
      .then(res => {
        console.log(res.data.items)
        news.value = res.data.items
      })
      .catch(err => console.log(err))
  }
  return { news, URL, getNews }
}, { persist: true })