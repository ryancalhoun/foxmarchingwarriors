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
  margin: 40px auto;
}
</style>
