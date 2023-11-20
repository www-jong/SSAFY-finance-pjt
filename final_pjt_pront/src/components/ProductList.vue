<template>
  <div>
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="loadDepositProducts">예금목록 보기</button>
    <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded" @click="loadSavingProducts">적금목록 보기</button>
    
    <LoadingPage v-if="loading.value" />

    <div v-else-if="showDepositList" class="mt-6">
      <table class="min-w-full divide-y divide-gray-200">
        <thead>
  <tr>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 60px;">Index</th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 150px;">은행명</th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">상품명</th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 105px;" @click="sortDeposits('6')">
      6개월
      <span v-if="DepositcurrentSort.term === '6' && DepositcurrentSort.direction === 'asc'">↑</span>
      <span v-else-if="DepositcurrentSort.term === '6' && DepositcurrentSort.direction === 'desc'">↓</span>
    </th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 105px;" @click="sortDeposits('12')">
      12개월
      <span v-if="DepositcurrentSort.term === '12' && DepositcurrentSort.direction === 'asc'">↑</span>
      <span v-else-if="DepositcurrentSort.term === '12' && DepositcurrentSort.direction === 'desc'">↓</span>
    </th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 105px;" @click="sortDeposits('24')">
      24개월
      <span v-if="DepositcurrentSort.term === '24' && DepositcurrentSort.direction === 'asc'">↑</span>
      <span v-else-if="DepositcurrentSort.term === '24' && DepositcurrentSort.direction === 'desc'">↓</span>
    </th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 105px;" @click="sortDeposits('36')">
      36개월
      <span v-if="DepositcurrentSort.term === '36' && DepositcurrentSort.direction === 'asc'">↑</span>
      <span v-else-if="DepositcurrentSort.term === '36' && DepositcurrentSort.direction === 'desc'">↓</span>
    </th>
  </tr>
</thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <DepositListItem 
            v-for="(product, index) in paginatedDeposits"
            :key="product.id"
            :product="product"
          />
        </tbody>
      </table>
      <Pagination :current-page="currentPage" :total-pages="totalDepositPages" @change-page="setPage" />
    </div>

    <div class="mt-6" v-else-if="showSavingList">
      <table class="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 60px;">Index</th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 150px;">은행명</th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">상품명</th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 105px;" @click="sortSavings('6')">
      6개월
      <span v-if="SavingcurrentSort.term === '6' && SavingcurrentSort.direction === 'asc'">↑</span>
      <span v-else-if="SavingcurrentSort.term === '6' && SavingcurrentSort.direction === 'desc'">↓</span>
    </th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 105px;" @click="sortSavings('12')">
      12개월
      <span v-if="SavingcurrentSort.term === '12' && SavingcurrentSort.direction === 'asc'">↑</span>
      <span v-else-if="SavingcurrentSort.term === '12' && SavingcurrentSort.direction === 'desc'">↓</span>
    </th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 105px;" @click="sortSavings('24')">
      24개월
      <span v-if="SavingcurrentSort.term === '24' && SavingcurrentSort.direction === 'asc'">↑</span>
      <span v-else-if="SavingcurrentSort.term === '24' && SavingcurrentSort.direction === 'desc'">↓</span>
    </th>
    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" style="width: 105px;" @click="sortSavings('36')">
      36개월
      <span v-if="SavingcurrentSort.term === '36' && SavingcurrentSort.direction === 'asc'">↑</span>
      <span v-else-if="SavingcurrentSort.term === '36' && SavingcurrentSort.direction === 'desc'">↓</span>
    </th>
  </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <SavingListItem 
            v-for="(product, index) in paginatedSavings"
            :key="product.id"
            :product="product"
          />
        </tbody>
      </table>
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

const DepositcurrentSort = ref({ term: null, direction: null });
const SavingcurrentSort = ref({ term: null, direction: null });

const loadDepositProducts = async () => {
  loading.value = true;
  await store.get_deposit_product();
  showDepositList.value = true;
  showSavingList.value = false;
  loading.value = false;
};

const loadSavingProducts = async () => {
  loading.value = true;
  await store.get_saving_product();
  showSavingList.value = true;
  showDepositList.value = false;
  loading.value = false;
};

const sortDeposits = (term) => {
  if (DepositcurrentSort.value.term === term) {
    DepositcurrentSort.value.direction = DepositcurrentSort.value.direction === 'asc' ? 'desc' : 'asc';
  } else {
    DepositcurrentSort.value = { term, direction: 'desc' };
  }
  applySort(store.deposit_products, DepositcurrentSort.value);
};

const sortSavings = (term) => {
  if (SavingcurrentSort.value.term === term) {
    SavingcurrentSort.value.direction = SavingcurrentSort.value.direction === 'asc' ? 'desc' : 'asc';
  } else {
    SavingcurrentSort.value = { term, direction: 'desc' };
  }
  applySort(store.saving_products, SavingcurrentSort.value);
};

const applySort = (products, sort) => {
  products.sort((a, b) => {
    const rateA = a.option.find(opt => opt.save_trm === sort.term)?.intr_rate || 0;
    const rateB = b.option.find(opt => opt.save_trm === sort.term)?.intr_rate || 0;
    return sort.direction === 'asc' ? rateA - rateB : rateB - rateA;
  });
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
};

</script>

<style scoped>
/* Tailwind CSS 스타일링 */
</style>
