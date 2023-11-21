<template>
  <header  v-if="!$route.meta.hideNav" class="bg-gray-800 text-white p-4">
    <nav class="flex justify-between items-center">
      <!-- Existing Links -->
      <div class="flex items-center space-x-4">
        <RouterLink class="hover:text-gray-300" :to="{ name: 'HomeView' }">Home</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{ name: 'KakaoView' }">은행 찾기</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{ name: 'ExChangeView' }">환율</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{ name: 'FinanceProductView' }">금융상품</RouterLink>
        
        <RouterLink class="hover:text-gray-300" :to="{ name: 'BoardView',params: { board_type: 'free' }}">자유게시판</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{ name: 'BoardView',params: { board_type: 'secret' }}">비밀게시판</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{ name: 'BoardView',params: { board_type: 'hi' }}">테스트게시판</RouterLink>
        <!-- Dropdown Wrapper -->

      </div>
      <div class="flex items-center space-x-4">
        <template v-if="store.isLogin">
          <RouterLink class="hover:text-gray-300" :to="{name:'AccountDetailView',params:{search_username:store.my_username}}">{{store.my_username}}님 환영합니다</RouterLink>
          <a type="button" @click="logOut"  class="hover:text-gray-300">Logout</a>
      </template>
      <template v-else>      
        <p>{{name}}</p>  
        <RouterLink class="hover:text-gray-300" :to="{name:'LogInView'}">LogIn</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{name:'SignUpView'}">SignUpPage</RouterLink>
      </template>
      </div>
      <!-- User Section -->
      <!-- ... Rest of the user section ... -->
    </nav>
  </header>
  <RouterView />
  <foot  v-if="!$route.meta.hideFoot"/>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';
import foot from '@/foot.vue'
const store = useCounterStore();
console.log('appvue')
const myname=store.username
const isDropdownOpen = ref(false);

const openDropdown = () => {
  isDropdownOpen.value = true;
};

const closeDropdown = () => {
  isDropdownOpen.value = false;
};

const logOut = () => {
  console.log('dd')
  store.logOut();
}

// ... Rest of your script ...
</script>

<style scoped>
/* Additional CSS styles can be defined here */
</style>
