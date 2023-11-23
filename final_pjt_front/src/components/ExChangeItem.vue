<template>
  <div class="p-4 bg-white shadow-md rounded-lg">
    <h5 class="text-lg font-semibold text-gray-700">{{ data.cur_nm }}</h5>
    <p class="text-gray-600 text-md">송금받을때 : {{ data.ttb }}</p>
    <p class="text-gray-600">송금보낼때 : {{ data.tts }}</p>
    <p class="text-gray-600">매매기준율 : {{ data.deal_bas_r }}</p>
  </div>
  <hr class="my-4">
</template>

<script setup>
import {RouterLink} from 'vue-router'
defineProps({
  data:Object
})
</script>
