<template>
  <div class="wrap">
    <div id="editor"/>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

import Quill from 'quill'
import ImageUploader from 'quill2-image-uploader'
import ImageResizor from 'quill-image-resizor'

const Link = Quill.import('formats/link');
Link.PROTOCOL_WHITELIST.push('webcal');

import 'quill/dist/quill.snow.css'

ImageResizor.Quill = Quill;
Quill.register('modules/imageUploader', ImageUploader);
Quill.register('modules/imageResizor', ImageResizor);

const { contents, onUpload } = defineProps(['contents', 'onUpload']);

const toolbar = [
  [{ 'header': [1, 2, 3, false] }],
  ['bold', 'italic', 'underline', 'strike'],
  [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
  [{ 'indent': '-1'}, { 'indent': '+1' }],
  [{ 'color': [] }, { 'background': [] }], 
  ['link'],
  ['image'],
];

let quill;
onMounted(() => {
  quill = new Quill('#editor', {
    theme: 'snow',
    modules: {
      toolbar: toolbar,
      imageUploader: { upload: onUpload },
      imageResizor: {}
    }
  });
  quill.setContents(contents);

  quill.on('text-change', () => contents.splice(0, Infinity, ...quill.getContents().ops));
});

</script>

<style scoped>
.wrap {
  height: 100%;
  display: flex;
  flex-direction: column;
}
#editor {
  flex-grow: 1;
}
</style>
