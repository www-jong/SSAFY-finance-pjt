<template>
  <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center">
    <!-- 모달 배경 -->
    <div class="fixed inset-0 bg-black bg-opacity-50" @click="closeModal"></div>

    <!-- 모달 내용 -->
    <div class="bg-white p-6 rounded-lg shadow-xl relative z-10 max-w-xl mx-auto">
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

      <div class="mt-4 flex justify-end">
        <button 
        v-if="!isSubscribed"
        @click="subscribe(product.code, option.save_trm)" 
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2">
        구독하기
      </button>
      <button 
        v-else 
        @click="unsubscribe(product.code, option.save_trm)" 
        class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mr-2">
        구독 취소하기
      </button>
        <button @click="closeModal()" class="text-blue-500 hover:text-blue-700">닫기</button>
        </div>
      </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits,computed } from 'vue';
import {useStore} from '@/stores/index'
import { routerKey,useRouter } from 'vue-router';
const router = useRouter()
const props = defineProps({
  option: Object,
  product:Object,
  showModal: Boolean,
  type:String
});
const store = useStore()
const emit = defineEmits(['update:showModal']);

// 사용자가 이미 구독했는지 확인
const isSubscribed = computed(() => {
  console.log('구독정보',props.product)
  return props.product.join_user.includes(store.my_id);
});

const subscribe = (code, save_trm) => {
  console.log("구독:", code, save_trm);
  store.join_product(props.type,code)
  closeModal()
  router.go(0);
};

const unsubscribe = (code, save_trm) => {
  console.log("구독 취소:", code, save_trm);
  store.join_product(props.type,code)
  closeModal()
  router.go(0);
};

const closeModal = () => {
  emit('update:showModal', false);
};
</script>

<style scoped>
/* 스타일링 추가 필요시 여기에 작성 */
</style>
