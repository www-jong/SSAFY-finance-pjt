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
    selectedCurrency: String,
    lineColor:String
});

const canvas = ref(null);
let chart = null;

onMounted(() => {
    console.log('라인컬러',props.lineColor)
    chart = new Chart(canvas.value.getContext('2d'), {
        type: 'line',
        data: props.chartData,
        options: {
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(100, 200, 200, 0.3)',
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
                    borderColor: props.lineColor,
                    borderWidth: 2,
                    ackgroundColor: `${props.lineColor}33`,
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

watch(() => props.lineColor, (newColor) => {
    if (chart) {
        chart.options.elements.line.borderColor = newColor;
        chart.options.elements.line.backgroundColor = `${newColor}33`;
        chart.update();
    }
});
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  max-width: 600px; /* 원하는 최대 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 (원하는 여백 설정) */
}
</style>
