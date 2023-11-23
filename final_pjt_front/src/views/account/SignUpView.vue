<template>
    <body class="bg-white font-family-karla h-screen">

        <div class="w-full flex flex-wrap">

            <!-- Register Section -->
            <div class="w-full md:w-1/2 flex flex-col">

                <div class="flex justify-center md:justify-start pt-12 md:pl-12 md:-mb-12">
                    <img src="@/assets/logo.png" class="text-white font-bold text-xl p-4 w-28">
                </div>
                <p class="text-center text-3xl">Join Us.</p>
                <div
                    class="flex flex-col justify-center md:justify-start my-auto pt-8 md:pt-0 px-8 md:px-24 lg:px-32 overflow-y-auto h-[75vh]">
                    <form @submit.prevent="signUp" class="flex flex-col pt-3 md:pt-8">
                        <!-- Username Field -->
                        <div class="flex flex-col pt-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="username">Username</label>
                            <input type="text" id="username" v-model.trim="username"
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                required>
                        </div>

                        <!-- Password Field -->
                        <div class="flex flex-col pt-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="password1">Password</label>
                            <input type="password" id="password1" v-model.trim="password1"
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                required>
                            <p v-if="!isPasswordValid" class="text-red-500 text-xs italic">Password must include both
                                letters and numbers.</p>
                        </div>

                        <!-- Password Confirmation Field -->
                        <div class="flex flex-col pt-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="password2">Password
                                Confirmation</label>
                            <input type="password" id="password2" v-model.trim="password2"
                                :class="{ 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline': true, 'border-red-500': !isPasswordMatch }"
                                required>
                            <p v-if="!isPasswordMatch" class="text-red-500 text-xs italic">Passwords do not match.</p>
                        </div>

                        <div class="flex flex-col pt-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="email">Email</label>
    <input type="email" id="email" v-model.trim="email"
           class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
           required>
</div>
                        <!-- Nickname Field -->
                        <div class="flex flex-col pt-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="nickname">Nickname</label>
                            <input type="text" id="nickname" v-model.trim="nickname"
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                required>
                        </div>

                        <div class="flex flex-col pt-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="birth">Birth Date</label>
                            <input type="date" max="2008-12-31" id="birth" v-model="birth" @input="handleBirthInput"
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                required>
                        </div>

                        <!-- Gender Field -->
                        <div class="flex flex-col pt-4">
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
<div class="flex flex-col pt-4 relative">
    <label for="capital" class="block text-gray-700 text-sm font-bold mb-2">자산</label>
    <input type="number" id="capital" v-model.number="capital" @input="validateCurrency"
           class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
    <span class="currency-label" v-if="capital">원(₩)</span>
</div>

<!-- Salary Field (Optional) -->
<div class="flex flex-col pt-4 relative">
    <label for="salary" class="block text-gray-700 text-sm font-bold mb-2">소득</label>
    <input type="number" id="salary" v-model.number="salary" @input="validateCurrency"
           class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
    <span class="currency-label" v-if="salary">원(₩)</span>
</div>



                        <input type="submit" value="SignUp"
                            class="bg-black text-white font-bold text-lg hover:bg-gray-700 p-2 mt-8" />
                    </form>
                    <div class="text-center pt-12 pb-12">
                        <p>이미 계정이 있으신가요? <RouterLink class="hover:text-gray-300" :to="{ name: 'LogInView2' }">LogIn
                            </RouterLink>
                        </p>
                    </div>
                </div>

            </div>

            <!-- Image Section -->
            <div class="w-1/2 shadow-2xl">
                <img class="object-cover w-full h-screen hidden md:block" src="@/assets/background.png"
                    alt="Background" />
            </div>
        </div>

    </body>
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
const capital = ref(0); // 선택 필드
const salary = ref(0); // 선택 필드

const isPasswordValid = computed(() => password1.value.length === 0 || (/[a-zA-Z]/.test(password1.value) && /[0-9]/.test(password1.value)));
const isPasswordMatch = computed(() => password2.value.length === 0 || password1.value === password2.value);
const store = useStore();
const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
const signUp = () => {
    if (!emailRegex.test(email.value)) {
        alert("올바른 이메일 형식이 아닙니다.");
        email.value = ''; // 입력 필드 비우기
        return
    }
    if (!isPasswordValid.value) {
        alert("비밀번호는 적어도 한개 이상의 문자, 한개 이상의 숫자가 있어야 합니다.");
        return;
    }
    if (!isPasswordMatch.value) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }
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

const MAX_CURRENCY_VALUE = 10000000000; // 최대값 설정


const validateCurrency = (event) => {
    const value = event.target.valueAsNumber;
    if (value > MAX_CURRENCY_VALUE) {
        alert("10000000000 이하의 값만 입력할 수 있습니다.");
        event.target.value = 0; // 입력 필드 비우기
    }
};


</script>
<style>
@import url('https://fonts.googleapis.com/css?family=Karla:400,700&display=swap');

.font-family-karla {
    font-family: karla;
}
.currency-label {
    position: absolute;
    right: 40px;
    top: 53px;
    font-size: 0.875rem;
    color: #4a5568;
}
</style>