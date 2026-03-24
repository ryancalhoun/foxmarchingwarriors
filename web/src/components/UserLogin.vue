<template>
  <form>
    <input type="text" v-model="email"/>
    <input type="password" v-model="password"/>
    <button type="submit" @click.prevent="login()">Login</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
const email = ref();
const password = ref();
async function login() {
  const result = await fetch('/api/authenticate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({ email: email.value, password: password.value }),
  });
}
</script>
