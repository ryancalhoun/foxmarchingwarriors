<template>
  <div v-if="page">
    <v-markdown-editor v-if='editing' v-model='changes' :upload-action="upload"/>
    <v-markdown-view v-else :content='page.contents'/>

    <div class="controls" v-if='user_token && editing'>
      <button @click.prevent="save"> <fa icon="fa-floppy-disk"/> Save </button>
      <button @click.prevent="cancel"> <fa icon="fa-circle-xmark"/> Cancel </button>
    </div>
    <div class="controls" v-if='user_token && !editing'>
      <button @click.prevent="edit"> <fa icon="fa-edit"/> Edit </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { VMarkdownView, VMarkdownEditor } from 'vue3-markdown'
import 'vue3-markdown/dist/vue3-markdown.css'

import { useAuth } from '@/components/Auth'

const { pages } = defineProps(['pages'])

const router = useRouter();
const route = useRoute();

const editing = ref(false);
const changes = ref();

const auth = useAuth();
const user_token = auth.getToken();

function getPage() {
  return pages.pages.find((p) => p.name == route.params.page);
}

const page = computed(() => {
  if(pages) {
    const p = getPage();
    if(p)
      return p;
    router.replace('/');
  }
});

function edit() {
  changes.value = page.value.contents;
  editing.value = true;
}

async function save() {
  const result = await fetch(`/api/pages/${page.value.name}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${user_token}`,
    },
    body: changes.value,
  });
  if(result.ok) {
    getPage().contents = changes.value;
    cancel();
  }
}

function cancel() {
  changes.value = '';
  editing.value = false;
}

function upload(file) {
}

</script>

<style scoped>
.controls {
  position: absolute;
  top: 12px;
  right: 0;
}
.controls button {
  background: none;
  border: none;
  cursor: pointer;
}
</style>
