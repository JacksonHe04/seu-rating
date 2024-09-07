<!-- src/components/Home.vue -->
<template>
  <BaseLayout>
    <AlbumResultCPN></AlbumResultCPN>
  </BaseLayout>
</template>

<script>
import BaseLayout from '../views/BaseLayout.vue';
import AlbumResultCPN from "@/components/AlbumResultCPN.vue";


export default {
  components: {
    AlbumResultCPN,
    BaseLayout,
  },
};
</script>