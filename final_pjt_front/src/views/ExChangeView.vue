<template>
  <main>
    <ExChange />
  </main>
</template>

<script setup>
import ExChange from '@/components/ExChange.vue'
import { onMounted } from 'vue'
import { useStore } from '@/stores/index'
const store = useStore()
onMounted(() => {
  store.getExChange()
})
</script>
