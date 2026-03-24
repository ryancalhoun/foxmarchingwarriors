<template>
  <div v-if="page">
    <v-markdown-view :content='page.contents'/>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { VMarkdownView } from 'vue3-markdown'

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
