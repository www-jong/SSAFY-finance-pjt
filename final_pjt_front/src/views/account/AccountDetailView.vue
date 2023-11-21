<template>
    <div v-if="filteredsearch_user" class="container mx-auto mt-10">
        <div class="p-16">
            <div class="p-8 bg-white shadow mt-24">
                <div class="grid grid-cols-1 md:grid-cols-3">
                    <div class="grid grid-cols-3 text-center order-last md:order-first mt-20 md:mt-0">
                        <div>
                            <p class="font-bold text-gray-700 text-xl">
                                {{ store.search_user_products ? store.search_user_products.length : 0 }}
                            </p>
                            <p class="text-gray-400">가입한 상품 수</p>
                        </div>
                        <div>
                            <p class="font-bold text-gray-700 text-xl">
                                {{ store.search_user_articles ? store.search_user_articles.length : 0 }}
                            </p>
                            <p class="text-gray-400">작성글</p>
                        </div>
                        <div>
                            <p class="font-bold text-gray-700 text-xl">
                                {{ store.search_user_comments ? store.search_user_comments.length : 0 }}
                            </p>
                            <p class="text-gray-400">작성 댓글</p>
                        </div>
                    </div>
                    <div class="relative">
                        <div
                            class="w-48 h-48 bg-indigo-100 mx-auto rounded-full shadow-2xl absolute inset-x-0 top-0 -mt-24 flex items-center justify-center text-indigo-500">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24" viewBox="0 0 20 20"
                                fill="currentColor">
                                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                                    clip-rule="evenodd" />
                            </svg>
                        </div>
                    </div>
                    <div class="space-x-8 flex justify-between mt-32 md:mt-0 md:justify-center">
                        <button v-if="isCurrentUser" @click="openModal"
                            class="text-white py-2 px-4 uppercase rounded bg-blue-400 hover:bg-blue-500 shadow hover:shadow-lg font-medium transition transform hover:-translate-y-0.5">
                            Edit Profile</button> <button
                            class="text-white py-2 px-4 uppercase rounded bg-gray-700 hover:bg-gray-800 shadow hover:shadow-lg font-medium transition transform hover:-translate-y-0.5">
                            Message</button>
                        <button v-if="isCurrentUser" @click="showDeleteConfirmation"
                            class="text-white py-2 px-4 uppercase rounded bg-gray-700 hover:bg-gray-800 shadow hover:shadow-lg font-medium transition transform hover:-translate-y-0.5">
                            탈퇴</button>
                    </div>

                </div>
                <div class="mt-20 text-center border-b pb-12">
                    <h1 class="text-4xl font-medium text-gray-700">{{ filteredsearch_user.nickname }} | {{
                        filteredsearch_user.gender === 'male' ? '남' : '여' }}</h1>
                    <p class="font-light text-gray-600 mt-3">{{ filteredsearch_user.birth }}</p>
                    <p class="mt-8 text-gray-500">email : {{ filteredsearch_user.email }}</p>
                    <p class="mt-8 text-gray-500">자금 : {{ filteredsearch_user.capital }}</p>
                    <p class="mt-8 text-gray-500">월급 : {{ filteredsearch_user.salary }}</p>
                </div>
                <div class="mt-12 flex flex-col justify-center">
                    <h2>가입 상품</h2>
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead>
      <tr>
        <th rowspan="2" class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          표시
        </th>
        <th rowspan="2" class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          은행명
        </th>
        <th rowspan="2" class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          상품명
        </th>
        <th colspan="2" class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          6개월
        </th>
        <th colspan="2" class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          12개월
        </th>
        <th colspan="2" class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          24개월
        </th>
        <th colspan="2" class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          36개월
        </th>
      </tr>
      <tr>
        <th class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          평균
        </th>
        <th class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          우대
        </th>
        <th class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          평균
        </th>
        <th class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          우대
        </th>
        <th class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          평균
        </th>
        <th class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          우대
        </th>
        <th class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          평균
        </th>
        <th class="px-6 py-3 bg-gray-50 text-center text-lg font-semibold text-gray-600 uppercase tracking-wider">
          우대
        </th>
      </tr>
    </thead>
                        <tbody>
                            <myProductListItem v-for="(product, index) in store.search_user_products" :key="product.id"
                                :product="product" @update:checked="handleChecked" />
                        </tbody>
                    </table>
                    <button class="text-indigo-500 py-2 px-4 font-medium mt-4"> Show more</button>
                </div>
            </div>
        </div>

        <ChartComponent v-if="chartData.datasets" :chartData="chartData" :options="chartOptions" />

    </div>
    <div v-else class="text-center">
        로딩중...
    </div>

    <AccountEditModal
      v-if="isModalOpen"
      :user="filteredsearch_user"
      @save="saveProfile"
      @cancel="closeModal"
    />
</template>

<script setup>
import { computed,reactive, ref, watch, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRoute, useRouter } from 'vue-router';
import myProductListItem from '@/components/myProductListItem.vue';
import AccountEditModal from '@/components/AccountEditModal.vue'
import { Chart } from 'chart.js';
import ChartComponent from '@/components/ChartComponent.vue';
const route = useRoute();
const router = useRouter();
const store = useCounterStore();
const isCurrentUser = computed(() => {
    return store.search_user && store.my_username && (store.search_user.username === store.my_username);
});

onMounted(() => {
    store.get_user_data(route.params.search_username, () => router.push('/'));
});

const filteredsearch_user = computed(() => store.search_user);

//watch(() => route.params.search_username, (newSearch_username) => {
//   store.get_user_data(newSearch_username, () => router.push('/'));
//});

const editProfile = () => {
    openEditModal

};

const followUser = () => {
    store.followUser(store.my_id, store.search_user.id);
    // 팔로우 로직
};

const showDeleteConfirmation = () => {
    while (true) {
        const userConfirmation = prompt("정말로 탈퇴하시겠어요? '탈퇴합니다'라고 입력하세요.");

        // 사용자가 취소 버튼을 누르거나 창을 닫으면 프롬프트가 null을 반환합니다.
        if (userConfirmation === null) {
            alert("회원 탈퇴가 취소되었습니다.");
            break; // 루프를 종료합니다.
        }

        if (userConfirmation === "탈퇴합니다") {
            store.account_delete();
            break; // 올바른 입력을 한 경우 루프를 종료합니다.
        } else {
            alert("문구가 틀립니다. 똑바로 입력하세요.");
        }
    }
};


const chartData = computed(() => {
    const labels = ['6개월', '12개월', '24개월', '36개월'];
    const filteredProducts = store.search_user_products.filter(product =>
        checkedProducts.value.includes(product.product.id)
    );
    console.log('####', filteredProducts)
    console.log(checkedProducts)
    const datasets = filteredProducts.map(product => {
        const data = labels.map(label => {
            const months = Number(label.split('개월')[0]);
            const option = product.option.find(o => o.save_trm === months);
            return option ? option.intr_rate : null;
        });


        return {
            label: product.product.fin_prdt_nm,
            data: data,
            // 색상 설정
        };
    });

    return {
        labels,
        datasets
    };
});

const chartOptions = {
    // 차트 옵션 설정
};

const checkedProducts = ref([]);

const handleChecked = ({ product, isChecked }) => {
    if (isChecked) {
        checkedProducts.value.push(product.id);
    } else {
        checkedProducts.value = checkedProducts.value.filter(id => id !== product.id);
    }
};


const isModalOpen = ref(false);

const openModal = () => {
  isModalOpen.value = true;
};

const closeModal = () => {
    console.log('닫아')
  isModalOpen.value = false;
};

const saveProfile = (editedUser) => {
  console.log('프로필 업데이트:', editedUser);
  closeModal();
};

</script>
  
<style>
/* 스타일은 여기에 추가 */
</style>
  