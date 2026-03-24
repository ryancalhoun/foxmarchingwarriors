<template>
  <load-pages v-slot="loaded">
    <nav-bar :pages="loaded.pages"/>
    <router-view :pages="loaded.pages"/>
  </load-pages>
</template>

<script setup>
import NavBar from '@/components/NavBar'
import LoadPages from '@/components/LoadPages'
import './assets/site.css'
</script>
