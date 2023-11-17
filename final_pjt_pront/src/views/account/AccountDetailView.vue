<template>
    <div v-if="search_user" class="container mx-auto mt-10">
        <!-- 유저 프로필 -->
        <div class="profile-header bg-white shadow p-6 rounded-lg">
            <!-- 이미지와 사용자 정보 표시 -->
            <div class="profile-info">
                <h2 class="text-2xl font-bold">{{ search_user.nickname }}</h2>
                <p class="text-gray-600">Followers: {{ search_user.followers | length }}</p>
                <p class="text-gray-600">Following: {{ search_user.followings | length }}</p>
            </div>
            <button v-if="isCurrentUser" @click="editProfile"
                class="edit-button bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Edit
                Profile</button>
            <button v-else @click="followUser"
                class="follow-button bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Follow</button>
        </div>

        <!-- 유저 상세 정보 -->
        <div class="profile-details bg-white shadow mt-4 p-6 rounded-lg">
            <h3 class="text-xl font-semibold mb-4">User Details</h3>
            <p><strong>Username:</strong> {{ search_user.username }}</p>
            <p><strong>Email:</strong> {{ search_user.email }}</p>
            <p><strong>Gender:</strong> {{ search_user.gender }}</p>
            <p><strong>Birth Date:</strong> {{ search_user.birth }}</p>
            <p><strong>Capital:</strong> {{ search_user.capital }}</p>
            <p><strong>Salary:</strong> {{ search_user.salary }}</p>
        </div>
    </div>
    <div v-else class="text-center">
        로딩중...
    </div>
</template>
  
  
<script setup>
import { computed, ref, watch,onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter'; // 스토어 경로 확인 필요
import { useRoute,useRouter } from 'vue-router'
const route = useRoute()
const router= useRouter()
const { search_user, currentUser } = useCounterStore();
const store = useCounterStore()
const isCurrentUser = computed(() => {
    return search_user.value && store.my_username && (search_user.value.username === store.my_username);
});


onMounted(() => {
  store.get_user_data(route.params.search_username, () => router.push('/'));
});

watch(() => route.params.search_username, (newSearch_username) => {
  store.get_user_data(newSearch_username, () => router.push('/'));
});
const editProfile = () => {
    // 프로필 수정 로직
};

const followUser = () => {
    // 팔로우 로직
};
</script>
  
<style></style>
  