<template>
    <div class="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-shadow">
      <!-- 간단한 표시 -->
      <div class="cursor-pointer" @click="toggleDetails">
        <h2 class="text-2xl font-semibold">{{ product.fin_prdt_nm }}</h2>
        <p class="text-gray-600">{{ product.kor_co_nm }}</p>
      </div>
      
      <!-- 세부 내용 -->
      <div v-if="showDetails">
        <hr class="my-4">
        <div class="flex justify-between">
          <div>
            <h3 class="text-lg font-semibold">가입 방법</h3>
            <p>{{ product.join_way }}</p>
          </div>
          <div>
            <h3 class="text-lg font-semibold">가입 대상</h3>
            <p>{{ product.join_member }}</p>
          </div>
        </div>
        <hr class="my-4">
        <h3 class="text-lg font-semibold">이자율</h3>
        <div v-html="formatInterestRate(product.mtrt_int)"></div>
        <hr class="my-4">
        <h3 class="text-lg font-semibold">특별 조건</h3>
        <p>{{ product.spcl_cnd }}</p>
        <hr class="my-4">
        <h3 class="text-lg font-semibold">가입 제한</h3>
        <p v-if="product.join_deny === '1'">가입 제한 있음</p>
        <p v-else>가입 제한 없음</p>
        <hr class="my-4">
        <h3 class="text-lg font-semibold">기타 정보</h3>
        <p>{{ product.etc_note }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps, ref } from 'vue'
  
  defineProps({
    product: Object,
  })
  
  const showDetails = ref(false)
  
  const toggleDetails = () => {
    showDetails.value = !showDetails.value
  }
  
  // 이자율 데이터 형식을 깔끔하게 포맷팅하는 함수
  const formatInterestRate = (interestRate) => {
    // 이 부분에서 이자율 데이터를 깔끔하게 포맷팅하는 로직을 추가해야 합니다.
    // 예: interestRate = "만기 후\n- 1개월이내 : 만기시점약정이율×50%\n- 1개월초과 6개월이내: 만기시점약정이율×30%\n- 6개월초과 : 만기시점약정이율×20%\n\n※ 만기시점 약정이율 : 일반정기예금 금리"
    // 위 데이터를 깔끔하게 포맷팅하여 반환해야 합니다.
  }
  </script>
  
  <style scoped>
  /* Tailwind CSS 스타일링을 여기에 추가할 수 있습니다. */
  </style>
  