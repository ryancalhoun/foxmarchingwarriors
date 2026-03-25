<template>
  <form>
    <div class="row" v-if="auth_result">
      {{ auth_result }}
    </div>
    <div class="row">
      <label> Email </label>
      <input type="text" v-model="email" :disabled="waiting || route.name == 'reset'"/>
    </div>
    <div class="row" v-if="route.name != 'reset'">
      <label> Password </label>
      <input type="password" v-model="password" :disabled="waiting"/>
    </div>
    <div class="row" v-if="route.name != 'login'">
      <label> New Password </label>
      <input type="password" v-model="new_password" :disabled="waiting"/>
    </div>
    <div class="row" v-if="route.name != 'login'">
      <label> Confirm Password </label>
      <input type="password" v-model="confirm_password" :disabled="waiting"/>
    </div>
    <div class="row">
      <button
        v-if="route.name == 'login'" type="submit" @click.prevent="login()"
        :disabled="waiting || !email || !password">
        Login
      </button>
      <button
        v-else-if="route.name == 'change'" type="submit" @click.prevent="change()"
        :disabled="waiting || !email || !password || !new_password || new_password != confirm_password">
        Change
      </button>
      <button
        v-else type="submit" @click.prevent="reset()"
        :disabled="waiting || !email || !code || !new_password || new_password != confirm_password">
        Reset
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute();
const { action } = defineProps(['action']);

const waiting = ref(false);
const code = ref(route.query.code);
const email = ref(route.query.email);
const password = ref();
const new_password = ref();
const confirm_password = ref();
const auth_result = ref();

async function auth(params) {
  waiting.value = true;
  const response = await fetch('api/authenticate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams(params),
  });

  if(response.ok) {
    return (await response.json()).auth;
  } else {
    password.value == null;
    new_password.value == null;
    confirm_password.value == null;
    auth_result.value = "Authentication error";
    waiting.value = false;
  }
}

async function login() {
  const token = auth({ email: email.value, password: password.value });
}
async function change() {
  const token = auth({ email: email.value, password: password.value, new_password: new_password.value });
}
async function reset() {
  const token = auth({ email: email.value, new_password: password.value, code: code.value });
}
</script>

<style scoped>
form {
  display: block;
  width: 32em;
  margin: 120px auto;
}
.row {
  margin-bottom: 12px;
  position: relative;
  height: 2em;
}
input, button {
  display: block;
  padding: 4px 12px;
  position: absolute;
  bottom: 0;
}
label {
  display: inline-block;
  width: 10em;
  text-align: right;
  position: absolute;
  bottom: 0.2em;
  left: -8px;
}
input {
  width: calc(100% - 12em);
  right: 0;
}
button {
  left: 12em;
}
</style>
