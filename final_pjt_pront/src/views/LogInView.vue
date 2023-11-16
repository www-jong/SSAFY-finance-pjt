<template>
  <div class="flex justify-center items-center h-screen bg-gray-100">
    <div class="w-full max-w-xs">
      <h1 class="mb-6 text-2xl font-semibold text-center text-gray-700">LogIn Page</h1>
      <form @submit.prevent="logIn" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="username">userid</label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" id="username" v-model.trim="username">
        </div>        
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password">Password</label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" type="password" id="password" v-model.trim="password">
        </div>
        <div class="flex items-center justify-between">
          <input class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit" value="LogIn">
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const username = ref('');
const password = ref('');

const store = useCounterStore();
const logIn = () => {
  const payload = {
    username: username.value,
    password: password.value
  };
  store.logIn(payload);
}
</script>

<style>
/* 여기에 필요한 추가 스타일을 정의할 수 있습니다 */
</style>
