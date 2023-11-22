<template>
    <div>
      <!-- 이미지 캐러셀 -->
      <div class="carousel-container relative">
    <div class="carousel flex transition-transform ease-in-out duration-300" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
      <div v-for="(img, index) in images" :key="index" class="carousel-item w-full flex-shrink-0">
        <img :src="img" alt="" class="w-full h-auto object-cover">
      </div>
    </div>
    <button class="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded-full shadow-lg z-10" @click="prevSlide">&lt;</button>
    <button class="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded-full shadow-lg z-10" @click="nextSlide">&gt;</button>
  </div>
  
  <div class="main-content container mx-auto px-4 mt-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
        <!-- 뉴스 리스트 섹션, lg 사이즈 이상에서 3/4 너비 -->
        <div class="lg:col-span-3">
          <NewsList/>
        </div>
    
        <!-- 오른쪽 칼럼, lg 사이즈 이상에서 1/4 너비 -->
        <div class="lg:col-span-1 space-y-4">
          <!-- 금융 상품 추천 섹션 -->
          <div class="financial-products bg-white p-4 rounded-lg shadow">
            금융 상품 추천
          </div>
    
          <!-- 오늘의 운세 섹션 -->
          <div class="daily-horoscope bg-white p-4 rounded-lg shadow" @click="showFortune">
        오늘의 운세
      </div>
        </div>
      </div>
    </div>
  
    <!-- 금 차트 섹션 -->
    <div class="gold-chart-container mx-auto px-4 my-8">
      <GoldChart/>
    </div>
  </div>
</template>
<script setup>
import NewsList from '@/components/NewsList.vue'
import GoldChart from '@/components/GoldChart.vue'
import { ref } from 'vue';
import background1 from '@/assets/background/background1.jpg';
import background2 from '@/assets/background/background2.jpg';
import background3 from '@/assets/background/background3.jpg';
import fortune_data from '@/assets/data/fortune.json'
const currentSlide = ref(0);

const images = ref([
  background1,
  background2,
  background3
]);
const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + images.value.length) % images.value.length;
};

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % images.value.length;
};
const fortuneMessages = fortune_data.data

const showFortune = () => {
  const randomIndex = Math.floor(Math.random() * fortuneMessages.length);
  alert(fortuneMessages[randomIndex]);
};
</script>

<style scoped>

.carousel {
    display: flex;
    transition: transform 0.3s ease-in-out;
}

.carousel-item {
    min-width: 100%;
}
.carousel-container {
  width: 100%;
  overflow: hidden;
}

.carousel-image {
  width: 100%;
  object-fit: cover;
}

.financial-products, .daily-horoscope {
  background: #ffffff;
  border-radius: 0.5rem; /* 둥근 모서리 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  padding: 1rem; /* 내부 여백 */
}


/* 이미지 높이를 500px로 고정하고 가로로 꽉 차게 설정 */
.carousel img {
  width: 100%;
  height: 500px; /* 또는 원하는 높이 */
  object-fit: cover;
}

.main-content, .gold-chart-container {
  max-width: 7xl; /* 또는 원하는 최대 너비 설정 */
  margin-left: auto;
  margin-right: auto;
  padding: 1rem; /* padding 값은 px-4 유틸리티에 해당 */
  margin-top: 2rem; /* mt-8 유틸리티에 해당 */
  margin-bottom: 2rem; /* my-8 유틸리티의 y- 부분에 해당 */
}
</style>