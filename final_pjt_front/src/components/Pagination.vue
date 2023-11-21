<template>
    <div class="flex justify-center items-center space-x-1">
        <!-- 첫 페이지로 이동 -->
        <button @click="emitPageChange(1)"
            class="px-3 py-1 bg-white border border-blue-500 rounded hover:bg-blue-500 hover:text-white"
            :disabled="currentPage === 1">
            첫 페이지
        </button>

        <!-- 이전 페이지 범위로 이동 -->
        <button @click="emitPageChange(Math.max(1, currentPage - 10))"
            class="px-3 py-1 bg-white border border-blue-500 rounded hover:bg-blue-500 hover:text-white"
            :disabled="currentPage <= 10">
            이전
        </button>

        <!-- 페이지 번호 버튼들 -->
        <button v-for="page in visiblePages" :key="page" @click="emitPageChange(page)"
            class="px-3 py-1 bg-white border border-blue-500 rounded hover:bg-blue-500 hover:text-white"
            :class="{ 'bg-blue-500 text-white': page === currentPage }">
            {{ page }}
        </button>

        <!-- 다음 페이지 범위로 이동 -->
        <button @click="emitPageChange(Math.min(totalPages, currentPage + 10))"
            class="px-3 py-1 bg-white border border-blue-500 rounded hover:bg-blue-500 hover:text-white"
            :disabled="currentPage > totalPages - 10">
            다음
        </button>

        <!-- 마지막 페이지로 이동 -->
        <button @click="emitPageChange(totalPages)"
            class="px-3 py-1 bg-white border border-blue-500 rounded hover:bg-blue-500 hover:text-white"
            :disabled="currentPage === totalPages">
            마지막 페이지
        </button>
    </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';

const props = defineProps({
    currentPage: Number,
    totalPages: Number,
});

const emits = defineEmits(['change-page']);

const visiblePageCount = 10;
const visiblePages = computed(() => {
    let startPage = Math.max(1, Math.floor((props.currentPage - 1) / visiblePageCount) * visiblePageCount + 1);
    const endPage = Math.min(startPage + visiblePageCount - 1, props.totalPages);

    return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
});

const emitPageChange = (page) => {
    if (page >= 1 && page <= props.totalPages) {
        emits('change-page', page);
    }
};
</script>