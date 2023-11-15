<template>
  <header class="bg-gray-800 text-white p-4">
    <nav class="flex justify-between items-center">
      <div class="flex items-center space-x-4">
        <RouterLink class="hover:text-gray-300" :to="{ name: 'HomeView' }">Home</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{ name: 'KakaoView' }">KakaoView</RouterLink>
      </div>
      <!-- 추가적인 네비게이션 메뉴나 로고 등을 여기에 배치할 수 있습니다 -->
      <div class="flex items-center space-x-4">
        <template v-if="store.isLogin">
          <p>{{store.original_username}}님 환영합니다</p> 
          <a type="button" @click="logOut"  class="hover:text-gray-300">Logout</a>
      </template>
      <template v-else>      
        <p>{{name}}</p>  
        <RouterLink class="hover:text-gray-300" :to="{name:'LogInView'}">LogIn</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{name:'SignUpView'}">SignUpPage</RouterLink>
      </template>
      </div>
    </nav>
  </header>
  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
import {useCounterStore} from '@/stores/counter'
const store=useCounterStore()
const name=store.original_username
console.log(store.original_username)
const logOut = () => {
  console.log('dd')
  store.logOut();
}
</script>

<style scoped>
/* 여기에 추가적인 CSS 스타일을 정의할 수 있습니다 */
</style>
