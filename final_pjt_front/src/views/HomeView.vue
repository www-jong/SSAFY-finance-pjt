<template>
    <div class="container mx-auto bg-gray-400 h-96 rounded-md flex items-center h-auto">
        <div class="carousel-container relative">
            <div class="carousel flex transition-transform ease-in-out duration-300"
                :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
                <div v-for="(img, index) in images" :key="index" class="carousel-item w-full flex-shrink-0">
                    <img :src="img" alt="" class="w-full h-auto object-cover">
                </div>
            </div>
            <button
                class="absolute left-0 top-1/2 transform -translate-y-1/2 bg-transparent p-10 h-full rounded-full shadow-lg z-10"
                @click="prevSlide">&lt;</button>
            <button
                class="absolute right-0 top-1/2 transform -translate-y-1/2 bg-transparent p-20 h-full rounded-full  z-10"
                @click="nextSlide">&gt;</button>
        </div>
    </div>

    <div class="py-6 container mx-auto px-6 md:px-0">
        <div>
            <div class="grid grid-cols-[3fr_1fr] gap-4 h-auto">
                <!-- 첫 번째 섹션 (2 프랙션 너비) -->
                <div>
                    <div class="bg-white border border-gray-300 shadow-lg rounded-lg h-auto pt-3">
                        <div>
                            <NewsList />
                        </div>
                    </div>
                </div>
                <!-- 두 번째 섹션 (1 프랙션 너비) -->
                <div>
                    <div class="grid grid-cols-1 gap-4">
                        <div>
                            <div class="bg-white border border-gray-300 shadow-lg rounded-lg h-48 overflow-hidden relative"
                                @click="recommend">
                                <div class="bg-white border border-gray-300 shadow-lg  h-36 overflow-hidden relative">
                                    <img src="@/assets/money.jpg" class="w-full h-full object-cover hover:blur-sm">
                                </div>
                                <div class="absolute bottom-0 left-0 right-0 flex justify-center">
                                    <span class="text-xl font-bold text-gray-800 bg-white p-2 rounded">
                                        금융상품 추천받기 
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div>
                            <div class="bg-white border border-gray-300 shadow-lg rounded-lg h-48 overflow-hidden relative"
                                @click="showFortune">
                                <div class="bg-white border border-gray-300 shadow-lg  h-36 overflow-hidden relative">
                                    <img src="@/assets/fortune.jpg" class="w-full h-full object-cover hover:blur-sm">
                                </div>
                                <div class="absolute bottom-0 left-0 right-0 flex justify-center">
                                    <span class="text-xl font-bold text-gray-800 bg-white p-2 rounded">
                                        오늘의 운세 확인하기
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div>
                            <div class="bg-gray border border-gray-300 shadow-lg rounded-lg h-48 overflow-hidden relative" @click="showFortune">
    <div class="container mx-auto px-6 md:px-0 h-full flex items-center justify-center">
        <div class="bg-white   rounded-lg p-1 max-w-xs mx-auto overflow-auto">
            <table class="min-w-full text-xs">
                <thead>
          <tr>
            <th class="px-2 py-1">순위</th>
            <th class="px-2 py-1">이름</th>
            <th class="px-2 py-1">가격(KRW)</th>
            <th class="px-2 py-1">총 시가</th>
            <th class="px-2 py-1">24시간 변동량</th> <!-- 새로운 열 추가 -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="coin in topCoins" :key="coin.id">
            <td class="border px-2 py-1">{{ coin.rank }}</td>
            <td class="border px-2 py-1">{{ coin.name }}</td>
            <td class="border px-2 py-1">{{ formatPrice(coin.quotes.KRW.price) }}</td>
            <td class="border px-2 py-1">{{ formatMarketCap(coin.quotes.KRW.market_cap) }}</td>
            <td class="border px-2 py-1">{{ coin.quotes.KRW.percent_change_24h }}%</td> <!-- 24시간 변동량 데이터 추가 -->
          </tr>
        </tbody>
            </table>
        </div>
    </div>
</div>

                        </div>
                    </div>
                </div>
            </div>

        </div>
        <div>
        </div>
    </div>

    <div class="container mx-auto px-6 md:px-0">
        <div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <a class=" font-bold ml-3 text-gray-600 mb-5">2개월간 금가격 추이</a>
                    <!-- Content for the first column -->
                    <div class="bg-white border border-gray-300 shadow-lg rounded-lg">
                        <GoldChart />
                    </div>
                </div>
                <div>
                    <div>
                        <a class=" font-bold  ml-3 text-gray-600 mb-5">1년간 은가격 추이</a>
                        <!-- Content for the first column -->
                        <div class="bg-white border border-gray-300 shadow-lg rounded-lg">
                            <SilverChart />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-if="isAlertVisible" class="custom-alert bg-white" @click="closeAlert">
        <div :class="['alert-content', alertBackgroundColor]">
            <p class="no-select">{{ alertMessage }}</p>
        </div>
    </div>
    <div v-if="isrecommendvisible && Array.isArray(rre) && rre.length === 3" class="custom-alert bg-white" @click="recommendclose">
    <div :class="['alert-content', alertBackgroundColor]">
        <p class="no-select text-left" v-for="(item, index) in rre" :key="index">{{ item }}</p>
        <p class="no-select text-left">을 추천드립니다.</p>
    </div>
</div>

</template>
<script setup>
import NewsList from '@/components/NewsList.vue'
import GoldChart from '@/components/GoldChart.vue'
import SilverChart from '@/components/SilverChart.vue'
import { ref, computed,onMounted } from 'vue';
import background1 from '@/assets/background/background1.jpg';
import background2 from '@/assets/background/background2.jpg';
import background3 from '@/assets/background/background3.jpg';
import fortune_data from '@/assets/data/fortune.json'
import fortune_inner from '@/assets/image.png'

import { useApiStore } from '@/stores/api'
import { useStore } from '@/stores/index'
const store = useStore()
const apistore = useApiStore()

const currentSlide = ref(0);

const images = ref([
    background1,
    background2,
    background3
]);
const prevSlide = () => {
    currentSlide.value = (currentSlide.value - 1 + images.value.length) % images.value.length;
};
const rre= computed(() => apistore.recommenditem)
const nextSlide = () => {
    currentSlide.value = (currentSlide.value + 1) % images.value.length;
};
const fortuneMessages = fortune_data.data


const isrecommendvisible=ref(false)
const isAlertVisible = ref(false);
const alertImage = fortune_inner // Set the default image path
const alertMessage = ref('');
const alertColor = ref('');
const alertBackgroundColor = computed(() => {
    switch (alertColor.value) {
        case 1: return 'bg-red-500';
        case 2: return 'bg-red-300';
        case 3: return 'bg-red-100';
        case 4: return 'bg-red-50';
        case 5: return 'bg-blue-100';
        case 6: return 'bg-blue-300';
        case 7: return 'bg-blue-500';
        default: return 'bg-white'; // 기본값
    }
});
// Function to show the alert with a message
const showFortune = () => {
    const randomIndex = Math.floor(Math.random() * fortuneMessages.length);
    alertMessage.value = fortuneMessages[randomIndex].content;
    alertColor.value = fortuneMessages[randomIndex].color;
    isAlertVisible.value = true;
};

const recommend = () => {
    apistore.recommend(store.my_id)
    isrecommendvisible.value=true
};
const recommendclose = () => {
    isrecommendvisible.value=false
}

// Function to close the alert
const closeAlert = () => {
    isAlertVisible.value = false;
};



const formatVolume = (volume) => {
    return `${(volume / 1e6).toFixed(2)}M`; // 예: 백만 단위로 표시
};
// 코인 데이터를 저장하기 위한 ref
const topCoins = ref([]);

// 숫자 포맷을 위한 함수
const formatPrice = (price) => {
    return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(price);
};

const formatMarketCap = (marketCap) => {
    return (marketCap / 1e12).toFixed(2) + 'T';
};

// API 호출을 통해 코인 데이터 가져오기
onMounted(async () => {
    try {
        const response = await fetch("https://api.coinpaprika.com/v1/tickers?quotes=KRW");
        const data = await response.json();
        topCoins.value = data.slice(0, 5);
    } catch (error) {
        console.error("Error fetching coin data:", error);
    }
});

</script>

<style scoped>
.no-select {
    user-select: none;
}

.blur-image {
    filter: blur(5px);
}

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
    height: 400px;
    /* 이미지 높이에 맞게 조절 (500px로 설정된 경우) */
}

.carousel-image {
    width: 100%;
    object-fit: cover;
}

.financial-products,
.daily-horoscope {
    background: #ffffff;
    border-radius: 0.5rem;
    /* 둥근 모서리 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    /* 그림자 효과 */
    padding: 1rem;
    /* 내부 여백 */
}


/* 이미지 높이를 500px로 고정하고 가로로 꽉 차게 설정 */
.carousel img {
    width: 100%;
    height: 500px;
    /* 또는 원하는 높이 */
    object-fit: cover;
}


.gold-chart-container {
    /* 또는 원하는 최대 너비 설정 */
    margin-left: auto;
    margin-right: auto;
    padding: 1rem;
    /* padding 값은 px-4 유틸리티에 해당 */
    margin-top: 2rem;
    /* mt-8 유틸리티에 해당 */
    margin-bottom: 2rem;
    /* my-8 유틸리티의 y- 부분에 해당 */
}

.custom-alert {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    /* semi-transparent background */
    display: flex;
    justify-content: center;
    align-items: center;
}

.alert-content {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}

.hidden {
    display: none;
}</style>