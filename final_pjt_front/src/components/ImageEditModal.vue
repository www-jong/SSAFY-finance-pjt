<template>
    <div class="modal fixed inset-0 flex items-center justify-center bg-black bg-opacity-50" @click="cancelEdit">
      <div class="modal-content bg-white p-6 rounded-lg shadow-lg" @click.stop>
        <h3 class="text-lg font-semibold mb-4">프로필 이미지 수정</h3>
        <!-- 현재 이미지 표시 -->
        <div>
    <img :src="user.image ? user.image : '/src/assets/default_profile_image.png'" alt="이미지 없음" class="w-24 h-24 mx-auto rounded-full object-cover"/>
  </div>
  
        <!-- 이미지 업로드 필드 -->
        <input type="file" @change="handleFileChange" accept="image/jpeg, image/png, image/jpg" class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"/>
  
        <!-- 버튼 그룹 -->
        <div class="flex justify-end mt-4">
          <button @click="saveProfile" class="bg-indigo-600 text-white px-4 py-2 rounded-md mr-2 hover:bg-indigo-700">저장</button>
          <button @click="cancelEdit" class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400">취소</button>
        </div>
      </div>
    </div>
  </template>
<script setup>
import { ref, defineProps, defineEmits, computed } from 'vue';
import { useStore } from '@/stores/index';

const store = useStore()
console.log('dd')


const props = defineProps({
    user: Object, // 편집할 사용자 정보
});
const editedUser = ref({ ...props.user });

const edit = () => {

    const payload = {
        image:none
    };
    store.account_image_edit(payload)
}

const selectedFile = ref(null);

const handleFileChange = (event) => {
    selectedFile.value = event.target.files[0];
};

const emit = defineEmits();

const saveProfile = () => {
    console.log('업로드 진행')
    if (selectedFile.value) {
        const formData = new FormData();
        formData.append('image', selectedFile.value);
        store.account_image_edit(formData)
    }else{
        alert('이미지를 업로드하세요.')
    }

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
