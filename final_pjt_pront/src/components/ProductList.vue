<template>
  <div>
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="loadDepositProducts">왼쪽 버튼</button>
    <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded" @click="loadSavingProducts">오른쪽 버튼</button>
    
    <!-- 로딩 중일 때 로딩 컴포넌트 표시 -->
    <LoadingPage v-if="loading" />

    <!-- 예금 상품 목록을 보여주는 코드 -->
    <div class="mt-6" v-else-if="showDepositList">
      <p>예금목록</p>
      <div class="space-y-4">
        <DepositListItem 
          v-for="(product, index) in filteredDeposits"
          :key="product.id"
          :product="product"
        />
      </div>
    </div>
    
    <!-- 적금 상품 목록을 보여주는 코드 -->
    <div class="mt-6" v-else-if="showSavingList">
      <p>적금목록</p>
      <div class="space-y-4">
        <SavingListItem 
          v-for="(product, index) in filteredSavings"
          :key="product.id"
          :product="product"
        />
      </div>
    </div>
    
    <!-- 로딩 메시지 -->
    <div v-else>
      게시글을 불러오는 중입니다...
    </div>
  </div>
</template>

<script setup>
import DepositListItem from '@/components/DepositListItem.vue'
import SavingListItem from '@/components/SavingListItem.vue'
import LoaingPage from '@/components/LoadingPage.vue' // 로딩 컴포넌트 추가
import { computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { onMounted, ref } from 'vue'

const store = useCounterStore()
const showDepositList = ref(false) // 예금 상품 목록을 보이게 할지 여부를 나타내는 변수
const showSavingList = ref(false) // 적금 상품 목록을 보이게 할지 여부를 나타내는 변수
const loading = ref(false) // 로딩 상태를 관리하기 위한 변수
let check = true

const loadDepositProducts = async () => {
  loading.value = true // 로딩 시작
  showDepositList.value = true
  showSavingList.value = false
  if (store.deposit_products.length > 0 || store.saving_products.length > 0) {
    check = false
  }
  await store.get_deposit_product(check) // 예금 상품 목록을 불러오는 비동기 함수 호출
  loading.value = false // 로딩 종료
  console.log('온')
}

const loadSavingProducts = async () => {
  loading.value = true // 로딩 시작
  showDepositList.value = false
  showSavingList.value = true
  if (store.deposit_products.length > 0 || store.saving_products.length > 0) {
    check = false
  }
  await store.get_saving_product(check) // 적금 상품 목록을 불러오는 비동기 함수 호출
  loading.value = false // 로딩 종료
}

const filteredDeposits = computed(() => store.deposit_products)
const filteredSavings = computed(() => store.saving_products)

// 컴포넌트가 마운트될 때 초기 데이터 로딩
onMounted(() => {
  console.log('컴포넌트가 마운트되었습니다.')
  // 초기 데이터 로딩 또는 필요한 초기 작업 수행
})
</script>

<style scoped>
/* Tailwind CSS 스타일링을 여기에 추가할 수 있습니다. */
</style>
