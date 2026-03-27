<template>
  <load-pages v-slot="loaded">
    <nav-bar :pages="loaded.pages"/>
    <router-view class="content" :pages="loaded.pages"/>
  </load-pages>
</template>

<script setup>
import NavBar from '@/components/NavBar'
import LoadPages from '@/components/LoadPages'
import './assets/site.css'
</script>

<style scoped>
.content {
  width: 960px;
  margin: 0 auto;
  padding: 40px 0;
  height: calc(100vh - 40px);
  position: relative;
}
</style>
