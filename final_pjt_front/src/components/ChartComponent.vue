<template>
    <div>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);
  
  const props = defineProps({
    chartData: Object,
    options: Object
  });
  
  const chartCanvas = ref(null);
  let chartInstance = null;
  
  const renderChart = () => {
    if (chartInstance) {
      chartInstance.destroy();
    }
    chartInstance = new Chart(chartCanvas.value, {
      type: 'bar',
      data: props.chartData,
      options: props.options
    });
  };
  
  onMounted(renderChart);
  watch(() => props.chartData, renderChart, { deep: true });
  </script>
  