<template>
  <div v-if="page">
    <edit-widget v-if='editing' :on-upload="upload" :contents="changes"/>
    <render-doc v-else :contents="page.contents"/>

    <calendar-events v-if="route.params.page == 'events'"/>

    <div class="controls" v-if="info && info.scopes && info.scopes.includes('edit')">
      <button @click.prevent="save" v-if="editing"> <fa icon="fa-floppy-disk"/> Save </button>
      <button @click.prevent="cancel" v-if="editing"> <fa icon="fa-circle-xmark"/> Cancel </button>
      <button @click.prevent="edit" v-if="!editing"> <fa icon="fa-edit"/> Edit </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/components/Auth'
import EditWidget from '@/components/EditWidget'
import RenderDoc from '@/components/RenderDoc'

import CalendarEvents from '@/components/CalendarEvents'

const router = useRouter();
const route = useRoute();

const page = ref();

watch(route, (to) => {
  page.value = null;
  cancel();
  load();
});

onMounted(() => {
  load();
});

const editing = ref(false);
const changes = ref();

const auth = useAuth();
const user_token = auth.getToken();
const info = auth.getAuthInfo();

async function edit() {
  changes.value = page.value.contents;
  editing.value = true;
}

async function load() {
  const result = await fetch(`/api/pages/${route.params.page}`);
  if(result.ok) {
    const p = await result.json();
    page.value = {
      v: p.v,
      contents: JSON.parse(p.contents),
    }
  }
}

async function save() {
  const result = await fetch(`/api/pages/${route.params.page}/${page.value.v}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${user_token}`,
    },
    body: JSON.stringify(changes.value),
  });
  if(result.ok) {
    page.value.contents = changes.value;
    page.value.v = (await result.json()).v;
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
