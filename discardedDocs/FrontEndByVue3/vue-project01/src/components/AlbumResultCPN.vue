<!-- src/components/AlbumResultCPN -->
<template>
  <div class="album_result_section layout_padding">
    <div v-if="album" class="album_result_container">
      <div class="musician_item">
        <div class="row align-items-center">
          <div class="col-3 pr-4">
            <div class="album_result_img">
              <img :src="album.cover_image" class="img-fluid" alt="album-img" />
            </div>
          </div>
          <div class="col-6 pr-4">
            <div class="album_result_title">
              <h1 class="album_title">{{ album.title }}</h1>
              <span>{{ album.artist }}</span>
            </div>
            <div class="album_rating row align-items-center">
              <div class="col-6">
                <p>SEU Rating: {{ album.rating }}</p>
              </div>
              <div class="col-6">
                <p>豆瓣评分: {{ album.douban_rating }}</p>
              </div>
            </div>
            <div class="album_intro">{{ album.introduction }}</div>
          </div>
          <div class="col-3">
            <h1 class="album_disc_title">专辑曲目</h1>
            <p v-for="track in album.tracks" :key="track">{{ track }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";

// 获取路由参数
const route = useRoute();
const albumId = route.params.albumId;

// 定义专辑数据
const album = ref(null);

// 请求专辑详细数据
const fetchAlbumData = async () => {
  try {
    const response = await axios.get(
      `http://localhost:8000/smrWeb/api/albums/${albumId}`,
    );
    album.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

// 当组件挂载时自动获取专辑数据
onMounted(() => {
  fetchAlbumData();
});
</script>
