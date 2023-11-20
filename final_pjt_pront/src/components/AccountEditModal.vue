<template>
    <div class="fixed inset-0 overflow-y-auto" v-if="showModal">
      <div class="flex items-center justify-center min-h-screen">
        <div class="modal-overlay fixed inset-0 bg-black opacity-50"></div>
  
        <div class="modal-container bg-white w-full max-w-md mx-auto rounded-lg shadow-lg z-50">
          <div class="modal-content p-4">
            <!-- 모달 내용 -->
            <h2 class="text-2xl font-bold">Edit Profile</h2>
            <!-- 수정할 내용 입력 폼 등을 추가하세요 -->
  
            <!-- 닫기 버튼 -->
            <button @click="closeModal" class="modal-close-button absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-lg">&times;</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const showModal = ref(false);
  
  const openModal = () => {
    showModal.value = true;
  };
  
  const closeModal = () => {
    showModal.value = false;
  };
  </script>
  