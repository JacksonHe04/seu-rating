<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="logo" href="/Home"
      ><img src="../assets/images/seuLogo2.jpeg" alt="SeuLogo" class="seuLogo"
    /></a>
    <button
      class="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarNav"
      aria-controls="navbarNav"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link" to="/Home">首页</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/SearchMusic">发现音乐</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/Albums">音乐专辑</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/Musicians">音乐人</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/Help">帮助</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/About">关于</router-link>
        </li>
      </ul>
    </div>
    <div class="login_text">
      <router-link to="/LogIn">登录</router-link>
    </div>
  </nav>
</template>
<script setup lang="ts"></script>
