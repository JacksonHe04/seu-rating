<!-- src/components/Home.vue -->
<template>
  <BaseLayout>
    <Search></Search>
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