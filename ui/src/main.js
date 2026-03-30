import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import {
  faBars,
  faCircleXmark,
  faEdit,
  faFloppyDisk,
  faLock,
  faLockOpen,
  faRightFromBracket,
  faTimes,
  faUser,
} from '@fortawesome/free-solid-svg-icons'

import { library } from '@fortawesome/fontawesome-svg-core'

library.add(
  faBars,
  faCircleXmark,
  faEdit,
  faFloppyDisk,
  faLock,
  faLockOpen,
  faRightFromBracket,
  faTimes,
  faUser,
)
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { Quill } from '@vueup/vue-quill'
import ImageUploader from 'quill-image-uploader'
import BlotFormatter from 'quill-blot-formatter'
Quill.register({imageUploader: ImageUploader});
//Quill.register({blotFormatter: BlotFormatter});

const app = createApp(App);
app.use(router);
app.component('fa', FontAwesomeIcon);

app.mount('#app');
