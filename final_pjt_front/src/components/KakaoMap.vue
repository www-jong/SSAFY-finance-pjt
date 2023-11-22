<template>
    <div class="map_wrap relative w-full h-screen">
        <!-- 지도 -->
        <div id="map"></div>

        <!-- 검색 옵션 및 결과 목록 -->
        <div id="menu_wrap"
            class="absolute top-0 left-0 bottom-0 w-90 m-2 p-2 overflow-y-auto bg-white rounded shadow-lg z-10">
            <div class="option">
                <select v-model="selectedSido" class="w-full mb-2 p-2 bg-gray-200 rounded">
                    <option disabled value="">시도를 선택하세요</option>
                    <option v-for="(value, name) in city_data" :key="name" :value="name">{{ name }}</option>
                </select>
                <select v-model="selectedSigungu" :disabled="!selectedSido" class="w-full mb-2 p-2 bg-gray-200 rounded">
                    <option disabled value="">시군구를 선택하세요</option>
                    <option v-for="name in sigungus" :key="name" :value="name">{{ name }}</option>
                </select>
                <select v-model="selectedEupmyeondong" :disabled="!selectedSigungu"
                    class="w-full mb-2 p-2 bg-gray-200 rounded">
                    <option disabled value="">읍면동을 선택하세요</option>
                    <option v-for="name in eupmyeondongs" :key="name" :value="name">{{ name }}</option>
                </select>
                <select v-model="selectedBank" :disabled="!selectedEupmyeondong"
                    class="w-full mb-2 p-2 bg-gray-200 rounded">
                    <option disabled value="">은행을 선택하세요</option>
                    <option v-for="(name, index) in bank_names" :key="name" :value="name" :selected="index === 0">{{ name }}</option>
                </select>
                <button @click="showSelection"
                    class="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-700">검색하기</button>
            </div>
            <hr class="my-2">
            <ul id="placesList">
                <li class="item" v-for="(result, index) in searchResults" :key="result.id" @click="moveToMarker(result)">
                    <span :class="'markerbg marker_' + (index + 1)"></span>
                    <div class="info">
                        <h5>{{ result.place_name }}</h5>
                        <span v-if="result.road_address_name">{{ result.road_address_name }}</span>
                        <span v-else>{{ result.address_name }}</span>
                        <span class="jibun gray" v-if="result.road_address_name">{{ result.address_name }}</span>
                        <span class="tel">{{ result.phone }}</span>
                    </div>
                    <hr>
                </li>
            </ul>
            <div id="pagination"></div>
        </div>
    </div>
</template>
<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import city_data from '@/assets/data/city_data.json'
import bank_data from '@/assets/data/banks.json'
console.log(city_data)
let selectedSido = ref('');
let selectedSigungu = ref('');
let selectedEupmyeondong = ref('');
let selectedBank =ref('')


// computed 속성을 사용하여 선택된 은행의 데이터를 가져옵니다.


const sigungus = computed(() => {
    if (!selectedSido.value) return [];
    return Object.keys(city_data[selectedSido.value]);
});

const eupmyeondongs = computed(() => {
    if (!selectedSigungu.value) return [];
    return city_data[selectedSido.value][selectedSigungu.value];
});
const bank_names = computed(() => {
    // Object.values()를 사용하여 bank_data["banks"]의 값을 배열로 변환
    const namesArray = Object.values(bank_data["banks"]);

    // sort() 메서드를 사용하여 배열을 알파벳 순으로 정렬
    namesArray.sort((a, b) => a.localeCompare(b));
    namesArray.unshift("--전체은행--");
    // 정렬된 배열 반환
    return namesArray;
});
const showSelection = () => {
    if(selectedBank.value==='--전체은행--'){
    searchPlaces(selectedSido.value + ' ' + selectedSigungu.value + ' ' + selectedEupmyeondong.value + ' 은행')
    }else{
        searchPlaces(selectedSido.value + ' ' + selectedSigungu.value + ' ' + selectedEupmyeondong.value + ' '+selectedBank.value)
    }
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
            //displaySearchResults(data);
            console.log('data!!', data)
            markers.value.forEach(marker => marker.setMap(null))
            markers.value = []
            data.forEach((place, idx) => {
                const imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png'
                const imageSize = new kakao.maps.Size(36, 37)
                const imgOptions = {
                    spriteSize: new kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
                    spriteOrigin: new kakao.maps.Point(0, (idx * 46) + 10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
                    offset: new kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
                }

                const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions)
                const marker = new kakao.maps.Marker({
                    map: map,
                    position: new kakao.maps.LatLng(place.y, place.x),
                    title: place.name,
                    image: markerImage

                });
                console.log(place.place_name)
                markers.value.push(marker)
                marker.setMap(map);
                searchResults.value = data

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
/*
const displaySearchResults = (data) => {
    searchResults.value = data.map(place => ({
        ...place,
        marker: new kakao.maps.Marker({
            map: map,
            position: new kakao.maps.LatLng(place.y, place.x)
        })
    }));
};
*/
const moveToMarker = (marker) => {
    console.log(marker)
    map.setCenter(new kakao.maps.LatLng(marker.y, marker.x));
};
</script>

<style scoped>
#map {
    width: 100%;
    height: 800px;
}
</style>

<style scoped>
#map {
    width: 100%;
    height: 800px;
}

.map_wrap,
.map_wrap * {
    margin: 0;
    padding: 0;
    font-family: 'Malgun Gothic', dotum, '돋움', sans-serif;
    font-size: 12px;
}

.map_wrap a,
.map_wrap a:hover,
.map_wrap a:active {
    color: #000;
    text-decoration: none;
}

.map_wrap {
    position: relative;
    width: 100%;
    height: 800px;
}

#menu_wrap {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 300px;
    margin: 10px 0 30px 10px;
    padding: 5px;
    overflow-y: auto;
    background: rgba(255, 255, 255, 0.7);
    z-index: 1;
    font-size: 12px;
    border-radius: 10px;
}

.bg_white {
    background: #fff;
}

#menu_wrap hr {
    display: block;
    height: 1px;
    border: 0;
    border-top: 2px solid #5F5F5F;
    margin: 3px 0;
}

#menu_wrap .option {
    text-align: center;
}

#menu_wrap .option p {
    margin: 10px 0;
}

#menu_wrap .option button {
    margin-left: 5px;
}

#placesList li {
    list-style: none;
}

#placesList .item {
    position: relative;
    border-bottom: 1px solid #888;
    overflow: hidden;
    cursor: pointer;
    min-height: 65px;
}

#placesList .item span {
    display: block;
    margin-top: 4px;
}

#placesList .item h5,
#placesList .item .info {
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
}

#placesList .item .info {
    padding: 10px 0 10px 55px;
}

#placesList .info .gray {
    color: #8a8a8a;
}

#placesList .info .jibun {
    padding-left: 26px;
    background: url("https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/places_jibun.png") no-repeat;
}

#placesList .item .markerbg {
    float: left;
    position: absolute;
    width: 36px;
    height: 37px;
    margin: 10px 0 0 10px;
    background: url("https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png") no-repeat;
}

#placesList .info .tel {
    color: #009900;
}


#placesList .item .marker_1 {
    background-position: 0 -10px;
}

#placesList .item .marker_2 {
    background-position: 0 -56px;
}

#placesList .item .marker_3 {
    background-position: 0 -102px
}

#placesList .item .marker_4 {
    background-position: 0 -148px;
}

#placesList .item .marker_5 {
    background-position: 0 -194px;
}

#placesList .item .marker_6 {
    background-position: 0 -240px;
}

#placesList .item .marker_7 {
    background-position: 0 -286px;
}

#placesList .item .marker_8 {
    background-position: 0 -332px;
}

#placesList .item .marker_9 {
    background-position: 0 -378px;
}

#placesList .item .marker_10 {
    background-position: 0 -423px;
}

#placesList .item .marker_11 {
    background-position: 0 -470px;
}

#placesList .item .marker_12 {
    background-position: 0 -516px;
}

#placesList .item .marker_13 {
    background-position: 0 -562px;
}

#placesList .item .marker_14 {
    background-position: 0 -608px;
}

#placesList .item .marker_15 {
    background-position: 0 -654px;
}

#pagination {
    margin: 10px auto;
    text-align: center;
}

#pagination a {
    display: inline-block;
    margin-right: 10px;
}

#pagination .on {
    font-weight: bold;
    cursor: default;
    color: #777;
}
</style>

<style>
</style>