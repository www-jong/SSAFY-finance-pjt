<template>
  <div v-if="isDataLoaded" class="p-4">
    <div class="mb-4">
      <select v-model="selectedCurrency" class="block p-2 border border-gray-200 rounded">
        <option value="USD (AM)">USD (AM)</option>
        <option value="USD (PM)">USD (PM)</option>
        <option value="GBP (AM)">GBP (AM)</option>
        <option value="GBP (PM)">GBP (PM)</option>
        <option value="EURO (AM)">EURO (AM)</option>
        <option value="EURO (PM)">EURO (PM)</option>
      </select>
    </div>

    <line-chart :chart-data="chartData" :selected-currency="selectedCurrency"></line-chart>
  </div>
  <div v-else class="p-4 text-center">
    데이터 로딩 중...
  </div>
</template>

<script setup>
import { ref, watchEffect, computed, onMounted } from 'vue';
import LineChart from '@/components/LineChart.vue';
import { useApiStore } from '@/stores/api';

const apiStore = useApiStore();
const selectedCurrency = ref('USD (AM)');
const chartData = ref([]);
const isDataLoaded = ref(false);

onMounted(async () => {
  await apiStore.getGold();
  isDataLoaded.value = true;
});

const goldPriceData = computed(() => {
  try {
    return JSON.parse(apiStore.golds);
  } catch (e) {
    return [];
  }
});

const convertTimestampToDate = (timestamp) => {
  const date = new Date(timestamp);
  return date.toISOString().split('T')[0]; // YYYY-MM-DD 형식
};

const transformChartData = () => {
  if (Array.isArray(goldPriceData.value) && goldPriceData.value.length > 0) {
    chartData.value = {
      labels: goldPriceData.value.map(item => convertTimestampToDate(item.Date)),
      datasets: [
        {
          label: selectedCurrency.value,
          data: goldPriceData.value.map(item => item[selectedCurrency.value]),
          // 스타일 설정
        }
      ]
    };
  } else {
    chartData.value = { labels: [], datasets: [] };
  }
};

watchEffect(transformChartData);
</script>
