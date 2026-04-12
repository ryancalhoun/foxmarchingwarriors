<template>
  <div>
    <h1> Users </h1>
    <table>
      <thead>
        <th> Last </th>
        <th> First </th>
        <th> Email </th>
        <th> Status </th>
        <th> Edit </th>
        <th> Users </th>
      </thead>
      <tbody>
        <tr v-for="user in users">
          <td> <input v-model="user.change_last"/> </td>
          <td> <input v-model="user.change_first"/> </td>

          <td> {{ user.email }} </td>

          <td v-if="user.password"> Ok </td>
          <td v-else-if="user.code"> Invited </td>

          <td v-if="user.scopes.includes('edit')"> Yes </td>
          <td v-else> No </td>

          <td v-if="user.scopes.includes('users')"> Yes </td>
          <td v-else> No </td>
        </tr>
      </tbody>
    </table>

    <button :disabled="!diffs()" @click.prevent="save()"> Save </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@/components/Auth'

const auth = useAuth();
const user_token = auth.getToken();
const info = auth.getAuthInfo();

const users = ref();
(async () => {
  users.value = (await (await fetch('/api/users', {
    headers: {
      Authorization: `Bearer ${user_token}`,
    },
  })).json()).users

  users.value.forEach((u) => {
    u.change_last = u.last;
    u.change_first = u.first;
  });
})();

function diffs() {
  return users.value && users.value.some((u) => u.change_last != u.last || u.change_first != u.first);
}

async function save() {
  users.value.forEach(async (u) => {
    const diff = {};
    if(u.change_last != u.last) {
      diff.last = u.change_last;
    }
    if(u.change_first != u.first) {
      diff.first = u.change_first;
    }

    if(Object.keys(diff).length > 0) {
      await fetch(`/api/users/${u.email}`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${user_token}`,
        },
        body: new URLSearchParams(diff),
      });

      u.last = u.change_last;
      u.first = u.change_first;
    }
  });
}

</script>

<style scoped>
th, td {
  text-align: left;
  padding-right: 20px;
  padding-bottom: 12px;
}
</style>
