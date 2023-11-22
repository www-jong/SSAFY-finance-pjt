<template>
  <div>
    <p v-if="position">Latitude: {{ position.latitude }}, Longitude: {{ position.longitude }}</p>
    <button @click="fetchLocation">현재 위치 가져오기</button>
  </div>
</template>

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