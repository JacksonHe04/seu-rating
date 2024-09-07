// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import AboutUs from '../views/About.vue';
import LogIn from '../views/LogIn.vue';
import SearchMusic from '../views/SearchMusic.vue';
import Albums from '../views/Albums.vue';
import MusicianResult from '../views/MusicianResult.vue';
import AlbumResult from '../views/AlbumResult.vue';
import Musicians from '../views/Musicians.vue';
import Help from '../views/Help.vue';

const routes = [
    { path: '/', component: Home, meta: { title: 'SEU Rating 首页' } },
    { path: '/home', component: Home, meta: { title: 'SEU Rating 首页' } },
    { path: '/musicianresult', component: MusicianResult, meta: { title: '音乐人结果' } },
    { path: '/albumresult', component: AlbumResult, meta: { title: '专辑结果' } },
    { path: '/searchmusic', component: SearchMusic, meta: { title: '发现音乐' } },
    { path: '/albums', component: Albums, meta: { title: '发现专辑' } },
    { path: '/musicians', component: Musicians, meta: { title: '音乐人' } },
    { path: '/help', component: Help, meta: { title: '帮助' } },
    { path: '/about', component: AboutUs, meta: { title: '关于' } },
    { path: '/login', component: LogIn, meta: { title: '登录' } },
];


const router = createRouter({
    history: createWebHistory(),
    routes,
});

// 动态设置页面 title
router.beforeEach((to, from, next) => {
    document.title = to.meta.title || 'SEU Rating';
    next();
});


export default router;