import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import {
  faBars,
  faCircleXmark,
  faEdit,
  faFloppyDisk,
  faTimes,
  faUser,
} from '@fortawesome/free-solid-svg-icons'

import { library } from '@fortawesome/fontawesome-svg-core'

library.add(
  faBars,
  faCircleXmark,
  faEdit,
  faFloppyDisk,
  faEdit,
  faTimes,
  faUser,
)
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const app = createApp(App);
app.use(router);
app.component('fa', FontAwesomeIcon);

app.mount('#app');
