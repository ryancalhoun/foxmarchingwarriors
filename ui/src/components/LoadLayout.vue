<template>
  <slot :layout="layout"></slot>
</template>

<script setup>
import { ref } from 'vue'
const layout = ref();

(async () => {
  const result = await fetch('/api/layout');
  if(result.ok) {
    layout.value = await(result.json());
  }
})();

</script>
