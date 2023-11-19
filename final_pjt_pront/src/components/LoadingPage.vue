<template>
  <div class="fixed inset-0 flex flex-col items-center justify-center bg-black bg-opacity-70 text-white">
    <!-- 로딩 스피너 -->
    <div class="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-32 w-32 mb-4"></div>
    <p>Loading...</p>
  </div>
</template>

<script>
export default {
  // 로딩 컴포넌트 로직
};
</script>

<style>
/* Tailwind CSS로 로딩 스피너 애니메이션 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loader {
  animation: spin 2s linear infinite;
}
</style>
