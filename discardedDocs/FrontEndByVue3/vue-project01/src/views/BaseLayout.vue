<!-- src/views/BaseLayout.vue -->
<template>
  <Nav></Nav>
  <slot></slot>
  <Footer></Footer>
</template>

<script>
import Nav from "@/components/Nav.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "BaseLayout",
  components: {
    Footer,
    Nav,
  },
};
</script>
