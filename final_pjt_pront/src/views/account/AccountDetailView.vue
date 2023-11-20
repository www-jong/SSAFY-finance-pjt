<template>
    <div v-if="filteredsearch_user" class="container mx-auto mt-10">
        <div class="p-16">
            <div class="p-8 bg-white shadow mt-24">
                <div class="grid grid-cols-1 md:grid-cols-3">
                    <div class="grid grid-cols-3 text-center order-last md:order-first mt-20 md:mt-0">
                        <div>
  <p class="font-bold text-gray-700 text-xl">
    {{ filteredsearch_user.financial_products ? filteredsearch_user.financial_products.length : 0 }}
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
                            </svg> </div>
                    </div>
                    <div class="space-x-8 flex justify-between mt-32 md:mt-0 md:justify-center">
                        <button v-if="isCurrentUser" @click="editProfile"
                            class="text-white py-2 px-4 uppercase rounded bg-blue-400 hover:bg-blue-500 shadow hover:shadow-lg font-medium transition transform hover:-translate-y-0.5">
                            Edit Profile</button> <button
                            class="text-white py-2 px-4 uppercase rounded bg-gray-700 hover:bg-gray-800 shadow hover:shadow-lg font-medium transition transform hover:-translate-y-0.5">
                            Message</button> 
                            <button  v-if="isCurrentUser" @click="showDeleteConfirmation"
                            class="text-white py-2 px-4 uppercase rounded bg-gray-700 hover:bg-gray-800 shadow hover:shadow-lg font-medium transition transform hover:-translate-y-0.5">
                            탈퇴</button> 
                        </div>
                </div>
                <div class="mt-20 text-center border-b pb-12">
                    <h1 class="text-4xl font-medium text-gray-700">{{ filteredsearch_user.nickname }} | {{ filteredsearch_user.gender === 'male' ? '남' : '여' }}</h1>
                    <p class="font-light text-gray-600 mt-3">{{ filteredsearch_user.birth }}</p>
                    <p class="mt-8 text-gray-500">email : {{ filteredsearch_user.email }}</p>
                    <p class="mt-8 text-gray-500">자금 : {{ filteredsearch_user.capital }}</p>
                    <p class="mt-8 text-gray-500">월급 : {{ filteredsearch_user.salary }}</p>
                </div>
                <div class="mt-12 flex flex-col justify-center">
                    <p class="text-gray-600 text-center font-light lg:px-16">An artist of considerable range, Ryan — the
                        name taken by Melbourne-raised, Brooklyn-based Nick Murphy — writes, performs and records all of his
                        own music, giving it a warm, intimate feel with a solid groove structure. An artist of considerable
                        range.</p> <button class="text-indigo-500 py-2 px-4  font-medium mt-4"> Show more</button>
                </div>
            </div>
        </div>




        <!-- 유저 프로필 -->
        <div class="profile-header bg-white shadow p-6 rounded-lg">
            <!-- 이미지와 사용자 정보 표시 -->
            <div class="profile-info">
                id : {{ filteredsearch_user.id }}
                <h2 class="text-2xl font-bold">{{ filteredsearch_user.nickname }}</h2>
                <p class="text-gray-600">Followers: {{ filteredsearch_user.followers.length }}</p>
                <p class="text-gray-600">Following: {{ filteredsearch_user.followings.length }}</p>
            </div>
            <button v-if="isCurrentUser" @click="editProfile"
                class="edit-button bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Edit Profile
            </button>
            <button v-else @click="followUser"
                class="follow-button bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Follow</button>
            <button v-if="isCurrentUser" @click="showDeleteConfirmation"
                class="delete-button bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded ml-2">Delete
                Account</button>
        </div>

    </div>
    <div v-else class="text-center">
        로딩중...
    </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRoute, useRouter } from 'vue-router';

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

watch(() => route.params.search_username, (newSearch_username) => {
    store.get_user_data(newSearch_username, () => router.push('/'));
});

const editProfile = () => {
    // 프로필 수정 로직

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

const deleteUserAccount = () => {
    // 회원 탈퇴 로직을 구현합니다. 예를 들어, API 호출을 통해 백엔드에 탈퇴 요청을 보낼 수 있습니다.
    // store.deleteUserAccount()와 같은 함수를 호출할 수도 있습니다.
};
</script>
  
<style>/* 스타일은 여기에 추가 */</style>
  