<template>
  <div v-if="user">
    <h1> Profile </h1>

    <p> Logged in as {{ user.email }}. </p>
    <ul>
      <li> <router-link :to="{ name: 'change' }"> <fa icon="fa-lock-open"/> Change password </router-link> </li>
      <li> <a href='#' @click.prevent="logout()"> <fa icon="fa-right-from-bracket"/> Logout </a> </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/components/Auth'

const router = useRouter();
const auth = useAuth();

const user = ref(auth.getAuthInfo());
if(! user.value) {
  router.push({name: 'login'});
}

function logout() {
  auth.logout();
  router.push('/');
}
</script>

<style scoped>
ul, li {
  list-style: none;
}
ul {
  margin-top: 80px;
}
li {
  height: 2em;
  font-size: 1.1em;
}
a {
  color: black;
  text-decoration: none;
}
svg {
  padding-right: 24px;
}
</style>
