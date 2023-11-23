<template>
    <ProductList class="mt-4" />
</template>

<script setup>
import { onMounted } from 'vue'
import { useStore } from '@/stores/index'
import { useRoute } from 'vue-router'
import ProductList from '@/components/ProductList.vue'
import { watch } from 'vue';

const route = useRoute()
const store = useStore()
console.log('views-board-type',route.params.board_type)
onMounted(() => {
  console.log('dd')
})

</script>

<style>

</style>
