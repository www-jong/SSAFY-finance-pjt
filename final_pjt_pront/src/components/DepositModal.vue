<template>
  <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center">
    <!-- 모달 배경 -->
    <div class="fixed inset-0 bg-black bg-opacity-50" @click="closeModal"></div>

    <!-- 모달 내용 -->
    <div class="bg-white p-6 rounded-lg shadow-xl relative z-10 max-w-lg mx-auto">
      <h2 class="text-2xl font-semibold mb-4">{{ product.fin_prdt_nm }}</h2>
      <p class="text-gray-600 mb-6">{{ product.kor_co_nm }}</p>

      <div class="my-4">
        <h3 class="text-lg font-semibold mb-2">옵션 상세 정보</h3>
        <ul>
          <li class="mb-1">저축 기간: {{ option.save_trm }}개월</li>
          <li class="mb-1">이자율: {{ option.intr_rate }}%</li>
          <li class="mb-1">이자율 종류: {{ option.intr_rate_type_nm }}</li>
        </ul>
      </div>

      <button @click="closeModal" class="text-blue-500 hover:text-blue-700 mt-4">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  option: Object,
  product:Object,
  showModal: Boolean,
});
const emit = defineEmits(['update:showModal']);

const closeModal = () => {
  emit('update:showModal', false);
};
</script>

<style scoped>
/* 스타일링 추가 필요시 여기에 작성 */
</style>
