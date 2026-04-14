<template>
  <load-layout v-slot="loaded">
    <nav-bar :layout="loaded.layout"/>
    <router-view class="content"/>
  </load-layout>
</template>

<script setup>
import NavBar from '@/components/NavBar'
import LoadLayout from '@/components/LoadLayout'
import './assets/site.css'
</script>

<style scoped>
.content {
  width: 100%;
  padding: 40px 16px;
  min-height: calc(100vh - 40px);
  position: relative;
}
@media screen and (min-width: 768px) {
  .content {
    max-width: 960px;
    margin: 0 auto;
  }
}

</style>
