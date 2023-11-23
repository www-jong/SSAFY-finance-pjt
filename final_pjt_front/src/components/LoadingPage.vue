<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-70">
    <img src="@/assets/coin.png" class="animate-spin h-30 w-30 rounded-full" alt="Loading">
  </div>
</template>
<script setup>
import { useStore } from '@/stores/index';
import { onMounted } from 'vue';

const store = useStore();

onMounted(() => {
  // 10초 후에 로딩 상태를 false로 설정
  setTimeout(() => {
    store.loading = false;
  }, 10000); // 10000 밀리초 = 10초
});

</script>

<style>
/* Tailwind CSS로 로딩 스피너 애니메이션 */
</style>