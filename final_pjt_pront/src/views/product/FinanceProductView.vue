<template>
    <h1>금융뷰</h1>
    <ProductList class="mt-4" />
</template>

<script setup>
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import ProductList from '@/components/ProductList.vue'
import { watch } from 'vue';

const route = useRoute()
const store = useCounterStore()
console.log('views-board-type',route.params.board_type)
onMounted(() => {
  console.log('dd')
  store.get_deposit_product()
})

</script>

<style>

</style>
