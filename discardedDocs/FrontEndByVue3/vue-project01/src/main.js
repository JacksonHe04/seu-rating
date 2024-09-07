// src/main.js
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

createApp(App).use(router).mount("#app");

// 引入全局 CSS 文件
import '@/assets/css/bootstrap.min.css';
import '@/assets/css/style.css';
import '@/assets/css/responsive.css';
import '@/assets/css/jquery.mCustomScrollbar.min.css';
import '@/assets/css/font-awesome.css';
import '@/assets/css/owl.carousel.min.css';
import '@/assets/css/owl.theme.default.min.css';
import '@/assets/css/jquery.fancybox.min.css';