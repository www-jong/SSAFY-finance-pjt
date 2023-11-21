<template>
  <tr>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
      <input type="checkbox" class="rounded text-indigo-600 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50" v-model="isChecked" @change="onCheckboxChange" />
    </td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 max-w-[200px]">{{ product.product.kor_co_nm}}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 max-w-[300px]">{{ product.product.fin_prdt_nm }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(6)">{{ getRate(6).init_rate }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(6)">{{ getRate(6).init_rate2 }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(12)">{{ getRate(12).init_rate }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(12)">{{ getRate(12).init_rate2 }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(24)">{{ getRate(24).init_rate }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(24)">{{ getRate(24).init_rate2 }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(36)">{{ getRate(36).init_rate }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(36)">{{ getRate(36).init_rate2 }}</td>
  </tr>
  <DepositModal 
    :product="product.product"
    :option="selectedOption"
    :showModal="showModal"
    :type="modal"
    @update:showModal="showModal = $event"
  />
</template>

<script setup>
import { defineProps, ref, computed,defineEmits } from 'vue'
import DepositModal from '@/components/DepositModal.vue'

const props = defineProps({
  product: Object,
})
const modal = 'deposit'
const showModal = ref(false)
const selectedOption = ref(null)
const getRate = (months) => {
  const option = props.product.option.find(o => o.save_trm == months);

  const intr_rate = option && option.intr_rate !== null ? `${option.intr_rate}%` : '--';
  const intr_rate2 = option && option.intr_rate2 !== null ? `${option.intr_rate2}%` : '--';

  return { init_rate: intr_rate, init_rate2: intr_rate2 };
};

const showOptionModal = (months) => {
  const option = props.product.option.find(o => o.save_trm == months)
  if (option) {
    selectedOption.value = option
    showModal.value = true
  }
}

const isChecked = ref(false);

const emit = defineEmits(['update:checked']);

// 체크박스 변경 핸들러
const onCheckboxChange = () => {
  console.log("check",props.product,isChecked.value)
  emit('update:checked', { product: props.product.product, isChecked: isChecked.value });
};

</script>

<style scoped>
/* 스타일링 */
</style>
