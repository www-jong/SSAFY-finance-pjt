<template>
  <div class="modal">
    <div class="modal-content">
      <h2>프로필 편집</h2>
      <div class="modal-scrollable-content ">
        <form @submit.prevent="saveProfile" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <!-- Username Field -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="username">Username</label>
          <input type="text" id="username" v-model.trim="editedUser.username" :placeholder="editedUser.username"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
        </div>

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
          <input type="password" id="password1" v-model.trim="editedUser.password1"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required>
          <p v-if="!isPasswordValid" class="text-red-500 text-xs italic">Password must include both letters and numbers.</p>
        </div>

        <!-- Password Confirmation Field -->
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password2">Password Confirmation</label>
          <input type="password" id="password2" v-model.trim="editedUser.password2"
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
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="capital">Capital</label>
          <input type="number" id="capital" v-model.number="editedUser.capital"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
        </div>

        <!-- Salary Field (Optional) -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="salary">Salary</label>
          <input type="number" id="salary" v-model.number="editedUser.salary"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
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

const props = defineProps({
  user: Object, // 편집할 사용자 정보
});

const editedUser = ref({ ...props.user }); // 편집을 위한 사용자 정보의 복사본을 만듭니다.
const existingPassword = ref('');
// 수정된 computed 속성 코드
const isPasswordValid = computed(() => {
  const password = editedUser.value.password1 || ''; // password1이 undefined인 경우 빈 문자열로 설정
  return password.length === 0 || (/[a-zA-Z]+/.test(password) && /[0-9]+/.test(password));
});
const isPasswordMatch = computed(() => editedUser.value.password1 === editedUser.value.password2);

const  emit  = defineEmits();

const saveProfile = () => {
  // 사용자 정보를 업데이트하기 위한 요청을 보냅니다. (editedUser 데이터 사용)
  // 성공적인 업데이트 후 모달을 닫습니다.
  emit('save', editedUser.value);
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

/* 프로필 편집 모달에 대한 추가적인 스타일을 적용할 수 있습니다. */
</style>
