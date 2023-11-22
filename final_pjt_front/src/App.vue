<template>

  <header  v-if="!$route.meta.hideNav" class="bg-gray-800 relative mb-1">
    <nav class="p-6 m-auto relative">
      <div class="flex justify-between items-center">
        <h1 class="pr-6 border-r-2 text-2xl font-bold text-gray-500">saunatime</h1>
        <div class="flex justify-between flex-grow">
          <div class="flex ml-6 items-center">
            <span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-4 cursor-pointer text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <input class="outline-none text-sm flex-grow bg-gray-100" type="text" placeholder="Search saunas in Finland…" />
          </div>
          <div class="md:flex space-x-6 hidden">
            <span class="text-gray-500 text-md">+ Add your sauna</span>
            <span class="text-gray-500 text-md">Sign up</span>
            <span class="text-gray-500 text-md">Log in</span>
          </div>
        </div>
      </div>
    </nav>

  </header>
  <main class="flex-grow mt-10 relative">
      <RouterView />
    </main>

    <foot v-if="!$route.meta.hideFoot" />

</template>

<script setup>
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import { useStore } from '@/stores/index';
import foot from '@/foot.vue'
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
  console.log('dd')
  store.logOut();
}

// ... Rest of your script ...
</script>


<style>
</style>