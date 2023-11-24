<template>
<body class="bg-white font-family-karla h-screen">

    <div class="w-full flex flex-wrap">

        <!-- Login Section -->
        <div class="w-full md:w-1/2 flex flex-col">

            <div class="flex justify-center md:justify-start pt-12 md:pl-12 md:-mb-24">
                <img src="@/assets/logo.png" class="text-white font-bold text-xl p-4 w-28">
            </div>

            <div class="flex flex-col justify-center md:justify-start my-auto pt-8 md:pt-0 px-8 md:px-24 lg:px-32">
                <p class="text-center text-3xl">Welcome.</p>
                <form class="flex flex-col pt-3 md:pt-8" @submit.prevent="logIn">
                    <div class="flex flex-col pt-4">
                        <label for="email" class="text-lg">username</label>
                        <input  placeholder="username" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mt-1 leading-tight focus:outline-none focus:shadow-outline" type="text" id="username" v-model.trim="username">
                    </div>
    
                    <div class="flex flex-col pt-4">
                        <label for="password" class="text-lg">Password</label>
                        <input placeholder="Password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mt-1 leading-tight focus:outline-none focus:shadow-outline" type="password" id="password" v-model.trim="password">
                    </div>
    
                    <input type="submit" value="Sign in" class="bg-black text-white font-bold text-lg hover:bg-gray-700 p-2 mt-8">
                </form>
                <div class="text-center pt-12 pb-12">
             <p><RouterLink class="hover:text-gray-300" :to="{name:'SignUpView'}"> Sign Up</RouterLink></p>
                </div>
            </div>

        </div>

        <!-- Image Section -->
        <div class="w-1/2 shadow-2xl">
            <img class="object-cover w-full h-screen hidden md:block" src="@/assets/background.png">
        </div>
    </div>

</body>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from '@/stores/index';

const username = ref('');
const password = ref('');

const store = useStore();
const logIn = () => {
  const payload = {
    username: username.value,
    password: password.value
  };
  store.logIn(payload);
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Karla:400,700&display=swap');

.font-family-karla {
    font-family: karla;
}
</style>