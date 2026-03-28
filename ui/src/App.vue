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
  width: 100%;
  padding: 40px 16px;
  height: calc(100vh - 40px);
  position: relative;
}
@media screen and (min-width: 768px) {
  .content {
    max-width: 960px;
    margin: 0 auto;
  }
}

</style>
