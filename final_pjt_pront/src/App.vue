<template>
  <header class="bg-gray-800 text-white p-4">
    <nav class="flex justify-between items-center">
      <!-- Existing Links -->
      <div class="flex items-center space-x-4">
        <RouterLink class="hover:text-gray-300" :to="{ name: 'HomeView' }">Home</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{ name: 'KakaoView' }">KakaoView</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{ name: 'ExChangeView' }">환율</RouterLink>
        <RouterLink class="hover:text-gray-300" :to="{ name: 'Board1View' }">자유게시판</RouterLink>
        <!-- Dropdown Wrapper -->
        <div class="relative" @mouseenter="openDropdown" @mouseleave="closeDropdown">
          <!-- Dropdown Trigger Button -->
          <button class="hover:text-gray-300">게시판</button>

          <!-- Dropdown Menu -->
          <div v-if="isDropdownOpen" class="absolute bg-gray-800 text-white shadow-lg rounded py-1 mt-2">
            <RouterLink class="hover:text-gray-300" :to="{ name: 'Board1View' }">자유게시판</RouterLink>
            <RouterLink class="hover:text-gray-300" :to="{ name: 'Board1View' }">자유게시판</RouterLink>
            <RouterLink class="hover:text-gray-300" :to="{ name: 'Board1View' }">자유게시판</RouterLink>
          </div>
        </div>
      </div>
      <!-- User Section -->
      <!-- ... Rest of the user section ... -->
    </nav>
  </header>
  <RouterView />
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const isDropdownOpen = ref(false);

const openDropdown = () => {
  isDropdownOpen.value = true;
};

const closeDropdown = () => {
  isDropdownOpen.value = false;
};

// ... Rest of your script ...
</script>

<style scoped>
/* Additional CSS styles can be defined here */
</style>
