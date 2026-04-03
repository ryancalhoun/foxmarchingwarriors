<template>
  <slot :pages="pages"></slot>
</template>

<script setup>
import { ref } from 'vue'
const pages = ref();

(async () => {
  const result = await (await fetch('/api/pages')).json();
  pages.value = {
    pages: result.pages.map((p) => {
      p.contents = JSON.parse(p.contents);
      return p;
    })
  };
})();

</script>
