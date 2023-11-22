<template>
  <div class="modal">
    <div class="modal-content">
      <h2>프로필 편집</h2>
      <div class="modal-scrollable-content ">
        <form @submit.prevent="saveProfile" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">

        <!-- Existing Password Field -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="existingPassword">Existing Password</label>
          <input type="password" id="existingPassword" v-model.trim="existingPassword"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
        </div>

        <!-- New Password Field -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password1">New Password</label>
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
          <input type="email" id="email" v-model.trim="editedUser.email"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
        </div>
        <!-- Nickname Field -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="nickname">Nickname</label>
          <input type="text" id="nickname" v-model.trim="editedUser.nickname"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
        </div>


        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="birth">Birth Date</label>
          <input type="date"  max="2008-12-31" id="birth" v-model="editedUser.birth"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
        </div>

        <!-- Gender Field -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="gender">Gender</label>
          <select id="gender" v-model="editedUser.gender"
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
    <input type="number" id="capital" v-model.number="editedUser.capital" @input="validateCurrency"
           class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
    <span class="currency-label" v-if="capital">원(₩)</span>
</div>

<!-- Salary Field (Optional) -->
<div class="flex flex-col pt-4 relative">
    <label for="salary" class="block text-gray-700 text-sm font-bold mb-2">소득</label>
    <input type="number" id="salary" v-model.number="editedUser.salary" @input="validateCurrency"
           class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
    <span class="currency-label" v-if="salary">원(₩)</span>
</div>



        <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          저장
        </button>
        <button @click="cancelEdit" class="bg-gray-400 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          취소
        </button>
      </form>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits,computed } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store=useCounterStore()
const existingPassword = ref('');
const password1 = ref('');
const password2 = ref('');
const email = ref('')
const nickname = ref('');
const birth = ref('');
const gender = ref('');
const capital = ref(0); // 선택 필드
const salary = ref(0); // 선택 필드

const props = defineProps({
  user: Object, // 편집할 사용자 정보
});
const editedUser = ref({ ...props.user });

const isPasswordValid = computed(() => password1.value.length === 0 || (/[a-zA-Z]/.test(password1.value) && /[0-9]/.test(password1.value)));
const isPasswordMatch = computed(() => password2.value.length === 0 || password1.value === password2.value);
const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
const edit = () => {
  console.log(editedUser)
  console.log('이멜',editedUser.value)
    if (!emailRegex.test(editedUser.value.email)) {
        alert("올바른 이메일 형식이 아닙니다.");
        editedUser.email.value = ''; // 입력 필드 비우기
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
        password1: password1.value,
        password2: password2.value,
        email: editedUser.value.email,
        nickname: editedUser.value.nickname,
        birth: editedUser.value.birth,
        gender: editedUser.value.gender,
        capital: editedUser.value.capital || 0,
        salary: editedUser.value.salary || 0,
        existingPassword:existingPassword.value
    };
    store.account_edit(payload)
}

const MAX_CURRENCY_VALUE = 10000000000; // 최대값 설정


const validateCurrency = (event) => {
    const value = event.target.valueAsNumber;
    if (value > MAX_CURRENCY_VALUE) {
        alert("10000000000 이하의 값만 입력할 수 있습니다.");
        event.target.value = 0; // 입력 필드 비우기
    }
};

const  emit  = defineEmits();

const saveProfile = () => {
  // 사용자 정보를 업데이트하기 위한 요청을 보냅니다. (editedUser 데이터 사용)
  // 성공적인 업데이트 후 모달을 닫습니다.
  edit()
  emit('save');
};

const cancelEdit = () => {
  // 변경사항을 저장하지 않고 모달을 닫습니다.
  emit('cancel');
};
</script>

<style scoped>
/* 모달에 대한 CSS 스타일을 추가합니다. */
.modal {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  overflow-y: auto; /* 스크롤이 필요한 경우에만 스크롤이 나타나도록 설정 */
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
  width: 80%; /* 모달 창의 폭을 조정합니다. */
  max-width: 400px; /* 모달 창의 최대 폭을 설정합니다. */
  margin: 0 auto; /* 가운데 정렬을 위해 margin을 추가합니다. */
}

.modal-scrollable-content {
  max-height: 70vh; /* 모달 내용의 최대 높이를 설정합니다. */
  overflow-y: auto; /* 내용이 넘칠 경우 스크롤이 나타나도록 설정 */
}

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
/* 프로필 편집 모달에 대한 추가적인 스타일을 적용할 수 있습니다. */
</style>
