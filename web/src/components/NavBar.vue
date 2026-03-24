<template>
  <nav>
    <router-link v-for="page in orderedPages" :to="page.name"> {{ page.name }} </router-link>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
const { pages } = defineProps(['pages']);
const orderedPages = computed(() => {
  if(pages) {
    return pages.pages.sort((a,b) => b.order - a.order)
  }
});
</script>

<style scoped>
nav {
  background: #222;
  width: 100%;
  height: 40px;
  padding: 4px 40px;
}
a {
  color: white;
}
</style>
