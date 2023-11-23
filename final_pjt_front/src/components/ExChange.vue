
<template>
  <div class="max-w-4xl mt-3 mx-auto p-4 bg-grey border border-gray-300 shadow-2xl rounded-lg">
    <h3 class="text-xl font-semibold text-blue-700 mb-6">환율정보</h3>
    <hr class="mb-6 border-blue-300">

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Left Column: Exchange Functionality -->
      <div>
        <div class="mb-6">
          <label class="block text-blue-700 text-sm font-bold mb-2" for="from_exchange">
            환전 출발 국가
          </label>
          <select v-model="from_exchange" id="from_exchange" class="shadow border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500">
            <option disabled value="">국가 선택</option>
            <option v-for="(value, name) in store.exchange_data" :key="value" :value="value">{{ value.cur_nm }}</option>
          </select>
          <input v-model="from_money" @input="updateFromMoney($event.target.value)" class="mt-3 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500" placeholder="금액 입력">
        </div>
        <div>
          <label class="block text-blue-700 text-sm font-bold mb-2" for="to_exchange">
            환전 도착 국가
          </label>
          <select v-model="to_exchange" id="to_exchange" class="shadow border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500">
            <option disabled value="">국가 선택</option>
            <option v-for="(value, name) in store.exchange_data" :key="value" :value="value">{{ value.cur_nm }}</option>
          </select>
          <input v-model="to_money" @input="updateToMoney($event.target.value)" class="mt-3 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500" placeholder="금액 입력">
        </div>
      </div>

<!-- Right Column: Country Data with Scroll -->
<div class="overflow-auto max-h-[600px]"> <!-- Set a max height and overflow auto -->
        <LoadingPage v-if="store.loading" />
        <div v-else>
          <div v-for="data in store.exchange_data" :key="data.cur_nm" class="mt-6">
            <ExChangeItem :data="data"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import ExChangeItem from '@/components/ExChangeItem.vue'
import {useStore} from '@/stores/index'
import { ref, watch } from 'vue';
import LoadingPage from '@/components/LoadingPage.vue';
const store = useStore()
const from_exchange = ref('')
const to_exchange = ref('')
const from_money = ref(0)
const to_money = ref(0)
const isUserTriggeredFrom = ref(false)
const isUserTriggeredTo = ref(false)

const calculateExchange = (amount, fromRate, toRate) => {
  // Remove commas and convert rates to numbers
  const cleanedFromRate = parseFloat(fromRate.replace(/,/g, ''));
  const cleanedToRate = parseFloat(toRate.replace(/,/g, ''));

  // Perform the calculation
  return (amount * cleanedFromRate) / cleanedToRate;
}
function to_Numeric(cur_unit) {
  // Forcefully convert cur_unit to a string
  const strUnit = String(cur_unit);

  // Use a regular expression to find digits
  const match = strUnit.match(/\d+/);

  if (match) {
    return parseInt(match[0], 10); // Convert the extracted string to a number
  }

  return 1; // Default to 1 if no digits are found
}

watch([from_money, from_exchange, to_exchange], ([newFromMoney]) => {
  if (isUserTriggeredFrom.value && from_exchange.value && to_exchange.value && newFromMoney) {
    console.log(from_exchange.value.cur_unit)
    const tmp_x=to_Numeric(from_exchange.value.cur_unit)
    console.log(tmp_x)
    to_money.value = calculateExchange(newFromMoney, from_exchange.value.deal_bas_r, to_exchange.value.deal_bas_r)/tmp_x.toFixed(2);
    isUserTriggeredFrom.value = false;
    console.log('감지',newFromMoney,from_exchange.value.deal_bas_r, to_exchange.value.deal_bas_r,newFromMoney*from_exchange.value.deal_bas_r/to_exchange.value.deal_bas_r)
  }
}, { deep: true });

watch([to_money, from_exchange, to_exchange], ([newToMoney]) => {
  if (isUserTriggeredTo.value && from_exchange.value && to_exchange.value && newToMoney) {
    const tmp_y=to_Numeric(from_exchange.value.cur_unit)
    from_money.value = calculateExchange(newToMoney, to_exchange.value.deal_bas_r, from_exchange.value.deal_bas_r)*tmp_y.toFixed(2);
    isUserTriggeredTo.value = false;
  }
}, { deep: true });

// 사용자 입력에 따른 플래그 업데이트 함수
function updateFromMoney(value) {
  isUserTriggeredFrom.value = true;
  from_money.value = value;
}

function updateToMoney(value) {
  isUserTriggeredTo.value = true;
  to_money.value = value;
}
</script>