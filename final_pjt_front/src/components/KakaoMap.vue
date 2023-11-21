<template>
    <div>
        <h2>장소 검색 테스트</h2>
        <select v-model="selectedSido">
            <option disabled value="">시도를 선택하세요</option>
            <option v-for="(value, name) in city_data" :key="name" :value="name">{{ name }}</option>
        </select>
        <select v-model="selectedSigungu" :disabled="!selectedSido">
            <option disabled value="">시군구를 선택하세요</option>
            <option v-for="name in sigungus" :key="name" :value="name">{{ name }}</option>
        </select>
        <select v-model="selectedEupmyeondong" :disabled="!selectedSigungu">
            <option disabled value="">읍면동을 선택하세요</option>
            <option v-for="name in eupmyeondongs" :key="name" :value="name">{{ name }}</option>
        </select>
        <button @click="showSelection">선택 완료</button>
        <div id="map"></div>
        <div id="searchResultsList">
    <ul>
        <li v-for="result in searchResults" :key="result.id" @click="moveToMarker(result.marker)">
            {{ result.place_name }}
        </li>
    </ul>
</div>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import city_data from '@/assets/data/city_data.json'
console.log(city_data)
let selectedSido = ref('');
let selectedSigungu = ref('');
let selectedEupmyeondong = ref('');

const sigungus = computed(() => {
    if (!selectedSido.value) return [];
    return Object.keys(city_data[selectedSido.value]);
});

const eupmyeondongs = computed(() => {
    if (!selectedSigungu.value) return [];
    return city_data[selectedSido.value][selectedSigungu.value];
});

const showSelection = () => {
    console.log(selectedSido.value + ' ' + selectedSigungu.value + ' ' + selectedEupmyeondong.value)
    searchPlaces(selectedSido.value + ' ' + selectedSigungu.value + ' ' + selectedEupmyeondong.value + ' ' + '은행')
    selectedSido.value = ''
    selectedSigungu.value = ''
    selectedEupmyeondong.value = ''

};
let places = null;
let map = null;
const searchkeyword = ref('')
const KAKAO_JS_KEY = import.meta.env.VITE_KAKAO_JS_API
const markers = ref([])
let searchResults = ref([]);



onMounted(() => {
    if (window.kakao && window.kakao.maps) {
        initMap();
    } else {
        const script = document.createElement('script');
        /* global kakao */
        script.onload = () => kakao.maps.load(initMap);
        script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${KAKAO_JS_KEY}&libraries=services,clusterer,drawing`;
        document.head.appendChild(script);
    }
});

const initMap = () => {
    const container = document.getElementById('map');
    const options = {
        center: new kakao.maps.LatLng(35.0879307, 128.9022845),
        level: 3,
    };

    map = new kakao.maps.Map(container, options);
    places = new kakao.maps.services.Places();
};

const searchPlaces = (searchkeyword) => {
    console.log(searchkeyword)
    if (markers.value.length > 0) {
        markers.value.forEach(marker => marker.setMap(null))
        markers.value = []
    }
    if (!searchkeyword.replace(/^\s+|\s+$/g, '')) {
        return;
    }

    places.keywordSearch(searchkeyword, (data, status) => {
        if (status === kakao.maps.services.Status.OK) {
            displaySearchResults(data);
            console.log('data!!', data)
            markers.value.forEach(marker => marker.setMap(null))
            markers.value = []
            data.forEach(place => {
                const marker = new kakao.maps.Marker({
                    map: map,
                    position: new kakao.maps.LatLng(place.y, place.x),
                    title: place.name,

                });
                console.log(place.place_name)
                markers.value.push(marker)
                marker.setMap(map);

                const infowindow = new kakao.maps.InfoWindow({
                    content: `<div>${place.place_name}</div>`
                })
                kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(map, marker, infowindow));
                kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow));
            });
            const coords = new kakao.maps.LatLng(data[0].y, data[0].x);
            map.setCenter(coords);
            // 여기에 검색 결과를 표시하는 로직을 추가합니다.
            console.log(data)
        } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
            alert('검색 결과가 존재하지 않습니다.');
        } else if (status === kakao.maps.services.Status.ERROR) {
            alert('검색 중 오류가 발생했습니다.');
        }
    });
};

// 인포윈도우를 표시하는 클로저를 만드는 함수입니다 
function makeOverListener(map, marker, infowindow) {
    return function () {
        infowindow.open(map, marker);
    };
}

// 인포윈도우를 닫는 클로저를 만드는 함수입니다 
function makeOutListener(infowindow) {
    return function () {
        infowindow.close();
    };
}

const displaySearchResults = (data) => {
    searchResults.value = data.map(place => ({
        ...place,
        marker: new kakao.maps.Marker({
            map: map,
            position: new kakao.maps.LatLng(place.y, place.x)
        })
    }));
};

const moveToMarker = (marker) => {
    map.setCenter(marker.getPosition());
};
</script>

<style scoped>
#map {
    width: 100%;
    height: 800px;
}
</style>