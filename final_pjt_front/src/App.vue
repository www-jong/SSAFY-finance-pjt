<template>
 <div class="app-container">
  <header  v-if="!$route.meta.hideNav" class="bg-gray-800 relative">
    <nav class="  relative">
      <div class="flex justify-between items-center">
        <RouterLink :to="{ name: 'HomeView' }">
        <img src="@/assets/logo.png"  class="text-white font-bold text-xl p-4 w-28">
      </RouterLink>
        <div class="flex justify-between flex-grow">
          <div class="flex ml-6 items-center">
            <span>
              <RouterLink class="text-gray-200 text-md hover:text-gray-500" :to="{ name: 'KakaoView' }">은행 찾기</RouterLink>
            </span>
            <span class="ml-8">
              <RouterLink class="text-gray-200 text-md hover:text-gray-500" :to="{ name: 'ExChangeView' }">환율</RouterLink>
            </span>
            <span class="ml-8">
              <RouterLink class="text-gray-200 text-md hover:text-gray-500" :to="{ name: 'FinanceProductView' }">예적금 비교</RouterLink>
            </span>
            <span class="ml-8">
              <RouterLink class="text-gray-200 text-md hover:text-gray-500" :to="{ name: 'BoardView',params: { board_type: 'notice' }}">주식게시판</RouterLink>
            </span>
            <span class="ml-8">
              <RouterLink class="text-gray-200 text-md hover:text-gray-500" :to="{ name: 'BoardView',params: { board_type: 'free' }}">비트코인게시판</RouterLink>
            </span>
            <span class="ml-8">
              <RouterLink class="text-gray-200 text-md hover:text-gray-500" :to="{ name: 'BoardView',params: { board_type: 'question' }}">자유게시판</RouterLink>
            </span>
          </div>
          <div class="md:flex mr-5 space-x-6 hidden">
            <RouterLink v-if="store.my_username" class="text-gray-200 text-md" :to="{name:'AccountDetailView',params:{search_username:store.my_username}}">{{store.my_nickname}}님 환영합니다</RouterLink>
            <a type="button" @click.prevent="logOut"  class="hover:text-gray-500 mr-4 text-gray-200 text-md">Logout</a>
          </div>

        </div>
      </div>
    </nav>

  </header>
  <main class="flex-grow relative">
      <RouterView />
    </main>

    <footer>
    <foot v-if="!$route.meta.hideFoot" />
  </footer>
</div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import { useStore } from '@/stores/index';
import foot from '@/foot.vue'
import { useRouter } from 'vue-router'

const router=useRouter()
const store = useStore();
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
  store.logOut();
  router.push({ name: 'LogInView' });
}
  


// ... Rest of your script ...
</script>
<style>
html, body {
  height: 100%;
  margin: 0;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex-grow: 1;
}

footer {
  flex-shrink: 0;
}
</style>