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
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/components/Auth'

const router = useRouter();
const route = useRoute();

const auth = useAuth();

const { action } = defineProps(['action']);

const waiting = ref(false);
const code = ref(route.query.code);
const email = ref(route.query.email || auth.getEmail());
const password = ref();
const new_password = ref();
const confirm_password = ref();
const auth_result = ref();

async function handleAuth(params) {
  try {
    waiting.value = true;
    await auth.submit(params);
    router.push('/');
  } catch(e) {
    auth_result.value = e.message;
    password.value == '';
    new_password.value == '';
    confirm_password.value == '';
    waiting.value = false;
  }
}

async function login() {
  await handleAuth({ email: email.value, password: password.value });
}
async function change() {
  await handleAuth({ email: email.value, password: password.value, new_password: new_password.value });
}
async function reset() {
  await handleAuth({ email: email.value, new_password: new_password.value, code: code.value });
}
</script>

<style scoped>
form {
  display: block;
  width: 100%;
}
.row {
  margin-bottom: 12px;
  position: relative;
  height: 4em;
}
label {
  display: block;
}
input {
  width: 100%;
}
button {
  left: 12em;
}
@media screen and (min-width: 768px) {
  form {
    width: 32em;
    margin: 120px auto;
  }
  input, button {
    display: block;
    padding: 4px 12px;
    position: absolute;
    bottom: 0;
  }
  input {
    width: calc(100% - 12em);
    right: 0;
  }
  label {
    display: inline-block;
    width: 10em;
    text-align: right;
    position: absolute;
    bottom: 0.2em;
    left: -8px;
  }
  .row {
    height: 2em;
  }
}
</style>
