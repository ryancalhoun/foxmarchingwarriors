<template>
  <nav>
    <div class="title">
      <router-link to="/" @click="menu = false">
        <img src="https://storage.googleapis.com/foxmarchingwarriors-static/logo.png"/>
        <span> foxmarchingwarriors </span>
      </router-link>
    </div>
    <div class="toggle">
      <a href="#" @click.prevent="toggle()">
        <fa :icon="menu ? 'times' : 'bars'"/>
      </a>
    </div>
    <div class="menu" :class="{ open: menu }" v-if="layout">
      <router-link v-for="page in layout.pages" :to="page"> {{ page }} </router-link>

      <div class="user">
        <router-link v-if="user" :to="{ name: 'user' }">
          <fa icon="fa-user"/>
          <span class="large-width"> profile </span>
        </router-link>
        <router-link v-else :to="{ name: 'login' }">
          <fa icon="fa-lock"/>
          login
        </router-link>

        <router-link v-if="user && user.scopes.includes('users')" :to="{ name: 'settings' }">
          <fa icon="fa-gear"/>
          <span class="large-width"> settings </span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/components/Auth'

const { layout } = defineProps(['layout']);

const menu = ref(false);

const auth = useAuth();
const user = ref(auth.getAuthInfo());

const router = useRouter();
const route = useRoute();
watch(route, (to) => {
  user.value = auth.getAuthInfo();
  menu.value = false;
});

function toggle() {
  menu.value = !menu.value;
}

</script>

<style scoped>
nav {
  background: #222;
  width: 100%;
  height: 40px;
  padding: 0 16px;
  position: sticky;
  top: 0;
  z-index: 1;
}
a {
  color: white;
  display: inline-block;
  text-decoration: none;
  line-height: 40px;
}

.title img {
  height: 24px;
  position: relative;
  bottom: -6px;
  border-radius: 50%;
}
.menu a {
  margin: 0 16px;
  text-transform: capitalize;
  display: block;
  height: 56px;
  line-height: 56px;
}

.menu {
  position: absolute;
  display: none;
  left: 0;
  width: 100%;
}
.menu.open {
  display: block;
  background: black;
  top: 40px;
}
.toggle {
  display: inline-block;
  position: absolute;
  right: 16px;
  bottom: 0;
}
@media screen and (min-width: 768px) {
  .toggle {
    display: none;
  }
  .title a :not(img) {
    display: none;
  }
  .menu {
    display: block;
    top: 0;
    padding-left: 40px;
  }
  .menu a {
    display: inline-block;
    height: 40px;
    line-height: 40px;
  }
  .menu .large-width {
    display: none;
  }
  .user {
    display: inline-block;
    position: absolute;
    right: 0;
  }
  .user a {
    margin: 0 8px;
  }
}
@media screen and (min-width: 1024px) {
  nav {
    padding: 0 40px;
  }
  .menu {
    padding-left: 80px;
  }
  .menu .large-width {
    display: initial;
  }
  .user {
    right: 20px;
  }
}

@media screen and (min-width: 1440px) {
  .menu {
    padding-left: 240px;
  }
  .menu a {
    margin: 0 24px;
  }
}
</style>
