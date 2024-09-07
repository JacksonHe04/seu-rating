<!-- src/components/Search.vue -->
<template>
  <div class="banner_section layout_padding">
    <div class="container">
      <h1 class="bestTitle">
        <slot name="bestTitle"> SEU Music Rating </slot>
      </h1>

      <slot name="searchBox">
        <div class="box_main">
          <slot name="input">
            <input
                v-model="musicianName"
                type="text"
                class="artist_bt"
                placeholder="请输入你想了解的音乐人"
                required
            />
          </slot>
          <button @click="searchMusician" class="search_bt">搜 索</button>
        </div>

        <p class="there_text">
          <slot name="there_text">
            你可以通过输入音乐人的名称，了解TA的相关信息以及TA最好的音乐作品
          </slot>
        </p>
      </slot>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  name: "Search",
  data() {
    return {
      musicianName: '', // 用户输入的音乐人名称
    };
  },
  methods: {
    async searchMusician() {
      if (this.musicianName) {
        try {
          const response = await axios.get(`http://127.0.0.1:8000/smrWeb/api/musicians/`, {
            params: { name: this.musicianName }
          });
          // 假设API返回了音乐人和专辑信息
          const musicianData = response.data;
          if (musicianData.musician) {
            // 将音乐家数据和专辑数据传递到MusicianResult页面
            this.$router.push({
              path: "/musicianresult",
              query: { name: this.musicianName }
            });
          } else {
            alert("未找到该音乐家");
          }
        } catch (error) {
          console.error(error);
        }
      } else {
        alert("请输入音乐家名称");
      }
    }
  }
};
</script>