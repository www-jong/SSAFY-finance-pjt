<template>
  <!-- <div class="flex justify-center items-center h-screen bg-gray-100"> -->
  <div class="pt-4 bg-gray-100"> 
    <!-- <div class="w-full max-w-xs"> -->
      <div class="w-full max-w-md mx-auto">
      <h1 class="mb-6 text-2xl font-semibold text-center text-gray-700">Sign Up Page</h1>
      <form @submit.prevent="signUp" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <!-- Username Field -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="username">Username</label>
          <input type="text" id="username" v-model.trim="username"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
        </div>

        <!-- Password Field -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password1">Password</label>
          <input type="password" id="password1" v-model.trim="password1"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
          <p v-if="!isPasswordValid" class="text-red-500 text-xs italic">Password must include both letters and numbers.</p>
        </div>

        <!-- Password Confirmation Field -->
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password2">Password Confirmation</label>
          <input type="password" id="password2" v-model.trim="password2"
            :class="{ 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline': true, 'border-red-500': !isPasswordMatch }"
            required>
          <p v-if="!isPasswordMatch" class="text-red-500 text-xs italic">Passwords do not match.</p>
        </div>

        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="email">Email</label>
          <input type="email" id="email" v-model.trim="email"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
        </div>
        <!-- Nickname Field -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="nickname">Nickname</label>
          <input type="text" id="nickname" v-model.trim="nickname"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
        </div>

        <!-- Birth Date Field -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="birth">Birth Date</label>
          <input type="date" id="birth" v-model="birth"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
        </div>

        <!-- Gender Field -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="gender">Gender</label>
          <select id="gender" v-model="gender"
            class="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
            <option value="" disabled>Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        <!-- Capital Field (Optional) -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="capital">Capital</label>
          <input type="number" id="capital" v-model.number="capital"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
        </div>

        <!-- Salary Field (Optional) -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="salary">Salary</label>
          <input type="number" id="salary" v-model.number="salary"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
        </div>

        <!-- Submit Button -->
        <div class="flex items-center justify-between">
          <input type="submit" value="SignUp"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useStore } from '@/stores/index';

const username = ref('');
const password1 = ref('');
const password2 = ref('');
const email = ref('')
const nickname = ref('');
const birth = ref('');
const gender = ref('');
const capital = ref(null); // 선택 필드
const salary = ref(null); // 선택 필드

const isPasswordValid = computed(() => password1.value.length === 0 || (/[a-zA-Z]/.test(password1.value) && /[0-9]/.test(password1.value)));
const isPasswordMatch = computed(() => password2.value.length === 0 || password1.value === password2.value);

const store = useStore();

const signUp = () => {
  if (!isPasswordValid.value) {
    alert("Password must include both letters and numbers.");
    return;
  }
  if (!isPasswordMatch.value) {
    alert("Passwords do not match.");
    return;
  }
  console.log('birth!!', birth)
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: email.value,
    nickname: nickname.value,
    birth: birth.value,
    gender: gender.value,
    capital: capital.value || 0,
    salary: salary.value || 0,
  };
  store.signUp(payload);
}
</script>

<style>/* 필요한 추가 스타일링 */</style>
