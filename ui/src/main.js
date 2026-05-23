import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import {
  faBars,
  faCircleXmark,
  faClipboardList,
  faEdit,
  faExternalLink,
  faFilePdf,
  faFloppyDisk,
  faGear,
  faLock,
  faLockOpen,
  faPaperclip,
  faRightFromBracket,
  faTimes,
  faUser,
} from '@fortawesome/free-solid-svg-icons'

import {
  faCalendarDays,
  faClone,
} from '@fortawesome/free-regular-svg-icons'

import { library } from '@fortawesome/fontawesome-svg-core'

library.add(
  faBars,
  faCalendarDays,
  faCircleXmark,
  faClipboardList,
  faClone,
  faEdit,
  faExternalLink,
  faFilePdf,
  faFloppyDisk,
  faGear,
  faLock,
  faLockOpen,
  faPaperclip,
  faRightFromBracket,
  faTimes,
  faUser,
)
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const app = createApp(App);
app.use(router);
app.component('fa', FontAwesomeIcon);

app.mount('#app');
