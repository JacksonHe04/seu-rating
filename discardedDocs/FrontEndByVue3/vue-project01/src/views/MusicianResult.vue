<!-- src/views/MusicianResult.vue -->
<template>
  <BaseLayout>
    <MusicianResultCPN></MusicianResultCPN>
  </BaseLayout>
</template>

<script>
import BaseLayout from '../views/BaseLayout.vue';
import MusicianResultCPN from "@/components/MusicianResultCPN.vue";


export default {
  components: {
    MusicianResultCPN,
    BaseLayout,
  },
};
</script>