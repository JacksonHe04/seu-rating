<!-- src/components/MusicianResultCPN -->
<template>
  <div class="musician_result_section layout_padding">
    <div class="container">
      <div v-if="musician" class="musician_item">
        <div class="row align-items-center">
          <div class="musician_5 col-5">
            <!-- 动态显示音乐人姓名 -->
            <h1 class="musician_title">{{ musician.name }}</h1>
            <div class="row align-items-center">
              <div class="col-4">
                <!-- 音乐人图片 -->
                <div class="musician_img">
                  <img :src="musician.image" alt="music-img" />
                </div>
              </div>
              <div class="col-8">
                <!-- 音乐人基本信息 -->
                <p
                  class="musician_info album_wrapper"
                  style="margin: 0; padding: 15px"
                >
                  {{ musician.info }}
                </p>
              </div>
            </div>
            <!-- 音乐人介绍 -->
            <p class="musician_intro album_wrapper">
              {{ musician.intro }}
            </p>
          </div>
          <div class="col-7">
            <!-- 显示专辑信息 -->
            <div
              v-for="(album, index) in albums"
              :key="album.id"
              class="album_row"
            >
              <div class="row">
                <div class="album_row_wrapper">
                  <div class="col-3">
                    <div class="album_row_img">
                      <img :src="album.cover_image" alt="album-img" />
                    </div>
                  </div>
                  <div class="col-9">
                    <div class="row">
                      <div class="col-3">
                        <h1 class="album_num">No.{{ index + 1 }}</h1>
                      </div>
                      <div class="col-9">
                        <!-- 动态显示专辑名称 -->
                        <h1 class="album_main">{{ album.title }}</h1>
                      </div>
                    </div>
                    <div class="row">
                      <div class="col-2">
                        <p class="ranking_main1" style="margin-right: 20px">
                          SEU Rating
                        </p>
                      </div>
                      <div class="col-3">
                        <!-- 动态显示专辑评分 -->
                        <p class="ranking_main2">{{ album.rating }}</p>
                      </div>
                      <div class="col-3">
                        <!-- 评分人数 -->
                        <p class="ranking_main3">
                          {{ album.rating_count }}人评分
                        </p>
                      </div>
                      <div class="col-4">
                        <div class="album_in_bt">
                          <div class="album_in_text">
                            <a @click="goToAlbumDetail(album.id)">查看详情</a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

// 定义数据
const musician = ref(null);
const albums = ref([]);
const router = useRouter();

// 请求音乐人数据
const fetchMusicianData = async (musicianName) => {
  try {
    const response = await axios.get(
        `http://localhost:8000/smrWeb/api/musicians/`,
        { params: { name: musicianName } } // 传递音乐人名称作为查询参数
    );
    musician.value = response.data.musician; // 音乐人数据
    albums.value = response.data.albums; // 专辑数据
  } catch (error) {
    console.error(error);
  }
};

// 当组件挂载时自动获取音乐人数据
onMounted(() => {
  const musicianName = router.currentRoute.value.query.name; // 从路由中获取音乐人名称
  fetchMusicianData(musicianName);
});

// 跳转到专辑详情页面
const goToAlbumDetail = (albumId) => {
  router.push({ path: `/albumresult/${albumId}` });
};
</script>
