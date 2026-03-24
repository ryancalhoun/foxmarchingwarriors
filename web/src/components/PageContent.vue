<template>
  <div v-if="page">
    {{ page.content }}
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const { pages } = defineProps(['pages'])

const router = useRouter();
const route = useRoute();

const page = computed(() => {
  if(pages) {
    const p = pages.pages.find((e) => e.name == route.params.page);
    if(p)
      return p;
    router.replace('/');
  }
});

</script>
