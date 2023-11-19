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
          v-for="(product, index) in paginatedDeposits"
          :key="product.id"
          :product="product"
        />
      </div>
      <Pagination :current-page="currentPage" :total-pages="totalDepositPages" @change-page="setPage" />
    </div>
    
    <!-- 적금 상품 목록을 보여주는 코드 -->
    <div class="mt-6" v-else-if="showSavingList">
      <p>적금목록</p>
      <div class="space-y-4">
        <SavingListItem 
          v-for="(product, index) in paginatedSavings"
          :key="product.id"
          :product="product"
        />
      </div>
      <Pagination :current-page="currentPage" :total-pages="totalSavingPages" @change-page="setPage" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import DepositListItem from '@/components/DepositListItem.vue';
import SavingListItem from '@/components/SavingListItem.vue';
import LoadingPage from '@/components/LoadingPage.vue';
import Pagination from '@/components/Pagination.vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const currentPage = ref(1);
const itemsPerPage = 10;
const loading = ref(false);
const showDepositList = ref(false);
const showSavingList = ref(false);

const loadDepositProducts = async () => {
  loading.value = true;
  showDepositList.value = true;
  showSavingList.value = false;

  let check = store.deposit_products.length === 0;
  await store.get_deposit_product(check);
  loading.value = false;
};

const loadSavingProducts = async () => {
  loading.value = true;
  showDepositList.value = false;
  showSavingList.value = true;

  let check = store.saving_products.length === 0;
  await store.get_saving_product(check);
  loading.value = false;
};

const paginatedDeposits = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return store.deposit_products.slice(start, end);
});

const paginatedSavings = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return store.saving_products.slice(start, end);
});

const totalDepositPages = computed(() => Math.ceil(store.deposit_products.length / itemsPerPage));
const totalSavingPages = computed(() => Math.ceil(store.saving_products.length / itemsPerPage));

const setPage = (page) => {
  currentPage.value = page;
  console.log(currentPage.value,page)
};

onMounted(loadDepositProducts);
</script>

<style scoped>
/* Tailwind CSS 스타일링 */
</style>
