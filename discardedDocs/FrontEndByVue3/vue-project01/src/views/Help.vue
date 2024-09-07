<!-- src/components/Home.vue -->
<template>
  <BaseLayout>
    <Search>
      <template v-slot:bestTitle>Help</template>
      <template v-slot:searchBox>
        <div></div>
      </template>
    </Search>
    <ForHelp></ForHelp>
  </BaseLayout>
</template>

<script>
import BaseLayout from '../views/BaseLayout.vue';
import SecondTitle from "@/components/SecondTitle.vue";
import Search from "@/components/Search.vue";
import AlbumsDiv from "@/components/AlbumsDiv.vue";
import ForHelp from "@/components/ForHelp.vue";

export default {
  components: {
    ForHelp,
    AlbumsDiv, Search, SecondTitle,
    BaseLayout,
  },
};
</script>