<template>
  <div v-if="page">
    <quill-editor v-if='editing'
      theme="snow"
      :toolbar="toolbar"
      :modules='modules'
      v-model:content='changes'
      contentType='html'/>

    <div v-else class="page-content" v-html="page.contents"/>

    <div class="controls" v-if="info && info.scopes && info.scopes.includes('edit')">
      <button @click.prevent="save" v-if="editing"> <fa icon="fa-floppy-disk"/> Save </button>
      <button @click.prevent="cancel" v-if="editing"> <fa icon="fa-circle-xmark"/> Cancel </button>
      <button @click.prevent="edit" v-if="!editing"> <fa icon="fa-edit"/> Edit </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { QuillEditor } from '@vueup/vue-quill'
import BlotFormatter from 'quill-blot-formatter'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

import { useAuth } from '@/components/Auth'

const { pages } = defineProps(['pages'])

const router = useRouter();
const route = useRoute();
watch(route, (to) => {
  cancel();
});

const editing = ref(false);
const changes = ref();

const auth = useAuth();
const user_token = auth.getToken();
const info = auth.getAuthInfo();

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

async function upload(file) {
  const data = new FormData();
  data.append('file', file);

  const response = await fetch(`/api/uploads/${page.value.name}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${user_token}`,
    },
    body: data,
  });

  return (await response.json()).url;
}

const toolbar = [
  [{ 'header': [1, 2, 3, false] }],
  ['bold', 'italic', 'underline', 'strike'],
  [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
  [{ 'indent': '-1'}, { 'indent': '+1' }],
  [{ 'color': [] }, { 'background': [] }], 
  ['image'],
];

const modules = [{
/*
  name: 'blotFormatter',
  module: BlotFormatter,
  options: { align }
}, {
*/
  name: 'imageUploader',
  module: ImageUploader,  
  options: { upload }
}];

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
img {
  max-width: 100%;
}
</style>
