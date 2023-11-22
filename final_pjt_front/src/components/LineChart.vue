<template>
<div class="chart-container">
        <canvas ref="canvas" style="position: relative;"></canvas>
    </div>
</template>
  
<script setup>
import { Chart, registerables } from 'chart.js';
import { ref, onMounted, watch } from 'vue';

Chart.register(...registerables);

const props = defineProps({
    chartData: Object,
    selectedCurrency: String
});

const canvas = ref(null);
let chart = null;

onMounted(() => {
    chart = new Chart(canvas.value.getContext('2d'), {
        type: 'line',
        data: props.chartData,
        options: {
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(200, 200, 200, 0.3)',
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(200, 200, 200, 0.3)',
                    }
                }
            },
            plugins: {
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function(context) {
                            const label = context.dataset.label || '';
                            const value = context.parsed.y;
                            return `${label}: ${value}`;
                        },
                        title: function(context) {
                            return context[0].label;
                        }
                    }
                },
                legend: {
                    display: false
                }
            },
            elements: {
                line: {
                    borderColor: '#FFD700',
                    borderWidth: 2,
                },
                point: {
                    radius: 0
                }
            }
        }
    });
});

watch(() => props.chartData, (newData) => {
    if (chart) {
        chart.data = newData;
        chart.update();
    }
}, { deep: true });
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  max-width: 800px; /* 원하는 최대 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 (원하는 여백 설정) */
}
</style>
