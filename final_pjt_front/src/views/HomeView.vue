<script setup>
import NewsList from '../components/NewsList.vue'


</script>

<template>

    <div>
        <h3>메인페이지입니다</h3>
        <p>여기에는 대략적인 서비스 소개 넣는거 어떨까요</p>
    </div>
    <NewsList/>

</template>

<style scoped>

</style>



<script>

<script setup>
import { ref } from 'vue';

const position = ref(null);

const fetchLocation = () => {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        position.value = {
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude
        };
      },
      (error) => {
        console.error("Error getting location: ", error);
      }
    );
  } else {
    console.error("Geolocation is not supported by this browser.");
  }
};
</script>