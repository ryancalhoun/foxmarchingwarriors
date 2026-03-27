<template>
  <div>
    <p> Logged in as {{ user }}. </p>

    <ul>
      <li> <router-link :to="{ name: 'change' }"> Change password </router-link> </li>
      <li> <a href='#' @click.prevent="logout()"> Logout </a> </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/components/Auth'

const router = useRouter();
const auth = useAuth();

const user = ref(auth.getEmail());
if(! user.value) {
  router.push({name: 'login'});
}

function logout() {
  auth.logout();
  router.push('/');
}
</script>
