<template>
  <tr>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ product.product.dcls_month }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 max-w-[200px]">{{ product.product.kor_co_nm }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 max-w-[300px]">{{ product.product.fin_prdt_nm }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(6)">{{ getRate(6) }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(12)">{{ getRate(12) }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(24)">{{ getRate(24) }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" @click="showOptionModal(36)">{{ getRate(36) }}</td>
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
import { defineProps, ref, computed } from 'vue'
import DepositModal from '@/components/DepositModal.vue'

const props = defineProps({
  product: Object,
})
const modal = 'deposit'
const showModal = ref(false)
const selectedOption = ref(null)

const getRate = (months) => {
  const option = props.product.option.find(o => o.save_trm == months)
  return option && option.intr_rate !== null ? `${option.intr_rate}%` : '--';
}


const showOptionModal = (months) => {
  const option = props.product.option.find(o => o.save_trm == months)
  if (option) {
    selectedOption.value = option
    showModal.value = true
  }
}

</script>

<style scoped>
/* 스타일링 */
</style>
