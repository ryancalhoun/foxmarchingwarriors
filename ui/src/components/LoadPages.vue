<template>
  <slot :pages="pages"></slot>
</template>

<script setup>
import { ref } from 'vue'
const pages = ref();

(async () => {
  pages.value = await (await fetch('/api/pages')).json();
})();

</script>
