<template>
  <div v-if="isDataLoaded" class="p-4">
    <div class="mb-4">
      <select v-model="selectedCurrency" class="block p-2 border border-gray-200 rounded">
        <option value="USD">USD</option>
        <option value="GBP">GBP</option>
        <option value="EURO">EURO</option>
      </select>
    </div>

    <line-chart 
    :chart-data="chartData" 
    :selected-currency="selectedCurrency"
    :lineColor="linecolor"></line-chart>
  </div>
  <div v-else class="p-4 text-center">
    데이터 로딩 중...
  </div>
</template>

<script setup>
import { ref, watchEffect, computed, onMounted } from 'vue';
import LineChart from '@/components/LineChart.vue';
import { useApiStore } from '@/stores/api';


const linecolor="#c0c0c0"
const apiStore = useApiStore();
const selectedCurrency = ref('USD');
const chartData = ref([]);
const isDataLoaded = ref(false);

onMounted(async () => {
  await apiStore.getSilver();
  isDataLoaded.value = true;
});

const silverPriceData = computed(() => {
  try {
    return JSON.parse(apiStore.silvers);
  } catch (e) {
    return [];
  }
});

const convertTimestampToDate = (timestamp) => {
  const date = new Date(timestamp);
  return date.toISOString().split('T')[0]; // YYYY-MM-DD 형식
};

const transformChartData = () => {
  if (Array.isArray(silverPriceData.value) && silverPriceData.value.length > 0) {
    chartData.value = {
      labels: silverPriceData.value.map(item => convertTimestampToDate(item.Date)),
      datasets: [
        {
          label: selectedCurrency.value,
          data: silverPriceData.value.map(item => item[selectedCurrency.value]),
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
