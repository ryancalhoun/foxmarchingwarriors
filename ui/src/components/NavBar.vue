<template>
  <nav>
    <div class="title">
      <router-link to="/" @click="menu = false">
        <img src="/logo.png"/>
        <span> foxmarchingwarriors </span>
      </router-link>
    </div>
    <div class="toggle">
      <a href="#" @click.prevent="toggle()">
        <fa :icon="menu ? 'times' : 'bars'"/>
      </a>
    </div>
    <div class="menu" :class="{ open: menu }">

      <router-link v-for="page in orderedPages" :to="page.name"> {{ page.name }} </router-link>

      <div class="user">
        <router-link v-if="user" :to="{ name: 'user' }"> <fa icon="fa-user"/> profile </router-link>
        <router-link v-else :to="{ name: 'login' }"> <fa icon="fa-lock"/> login </router-link>

        <router-link v-if="user && user.scopes.includes('users')" :to="{ name: 'settings' }"> <fa icon="fa-gear"/> </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/components/Auth'

const { pages } = defineProps(['pages']);

const orderedPages = computed(() => {
  if(pages) {
    return pages.pages.sort((a,b) => a.order - b.order)
  }
  return [];
});

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
  position: relative;
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
  bottom: -8px;
  border-radius: 50%;
}
.menu a {
  margin: 0 24px;
  text-transform: capitalize;
  display: block;
  height: 40px;
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
  nav {
    padding: 0 40px;
  }
  .toggle {
    display: none;
  }
  .title a :not(img) {
    display: none;
  }
  .menu {
    display: block;
    top: 0;
    padding-left: 240px;
  }
  .menu a {
    display: inline-block;
  }
  .user {
    display: inline-block;
    position: absolute;
    right: 20px;
  }
}
</style>
