<!-- src/components/SearchMusic.vue -->
<template>
  <BaseLayout>
    <Search>
      <template v-slot:bestTitle>Search Music</template>
      <template v-slot:input>
        <input
            type="text"
            class="artist_bt"
            placeholder="请输入你想了解的音乐及其作者"
            name="query"
            required
        />
      </template>
      <template v-slot:there_text>你可以这样输入，例如：晴天 周杰伦，以了解该音乐作品的信息</template>
    </Search>
    <SecondTitle></SecondTitle>
    <AlbumsDiv></AlbumsDiv>
  </BaseLayout>
</template>

<script>
import BaseLayout from '../views/BaseLayout.vue';
import SecondTitle from "@/components/SecondTitle.vue";
import Search from "@/components/Search.vue";
import AlbumsDiv from "@/components/AlbumsDiv.vue";

export default {
  components: {
    AlbumsDiv, Search, SecondTitle,
    BaseLayout,
  },
};
</script>