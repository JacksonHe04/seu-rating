<!-- src/components/Musicians.vue -->
<template>
  <BaseLayout>
    <Search>
      <template v-slot:bestTitle>Musicians</template>
      <template v-slot:input>
        <input
            type="text"
            class="artist_bt"
            placeholder="请输入你想了解的音乐人"
            name="query"
            required
        />
      </template>
      <template v-slot:there_text>你可以这样输入，例如：Taylor Swift，以了解该音乐人的信息</template>
    </Search>
    <SecondTitle>
      <template v-slot:secondTitle>Musicians</template>
    </SecondTitle>
    <MusiciansDiv></MusiciansDiv>
  </BaseLayout>
</template>

<script>
import BaseLayout from '../views/BaseLayout.vue';
import SecondTitle from "@/components/SecondTitle.vue";
import Search from "@/components/Search.vue";
import AlbumsDiv from "@/components/AlbumsDiv.vue";
import MusiciansDiv from "@/components/MusiciansDiv.vue";

export default {
  components: {
    MusiciansDiv,
    AlbumsDiv, Search, SecondTitle,
    BaseLayout,
  },
};
</script>