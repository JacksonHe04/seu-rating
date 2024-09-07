<!-- src/components/Home.vue -->
<template>
  <BaseLayout>
    <Search>
      <template v-slot:bestTitle>About Us</template>
      <template v-slot:searchBox>
        <div></div>
      </template>
    </Search>
    <AboutUs></AboutUs>
  </BaseLayout>
</template>

<script>
import BaseLayout from "../views/BaseLayout.vue";
import Search from "@/components/Search.vue";
import AboutUs from "@/components/AboutUs.vue";

export default {
  components: {
    AboutUs,
    Search,
    BaseLayout,
  },
};
</script>
