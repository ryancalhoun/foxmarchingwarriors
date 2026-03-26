<template>
  <nav>
    <router-link v-for="page in orderedPages" :to="page.name"> {{ page.name }} </router-link>

    <div class="user">
      <router-link v-if="user" :to="{ name: 'user' }"> <fa icon="fa-user"/> </router-link>
      <router-link v-else :to="{ name: 'login' }"> login </router-link>
    </div>
  </nav>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAuth } from '@/components/Auth'

const { pages } = defineProps(['pages']);

const orderedPages = computed(() => {
  if(pages) {
    return pages.pages.sort((a,b) => a.order - b.order)
  }
});

const auth = useAuth();
const user = ref(auth.getEmail());

</script>

<style scoped>
nav {
  background: #222;
  width: 100%;
  height: 40px;
  padding: 4px 20px;
  position: relative;
}
a {
  color: white;
  display: inline-block;
  margin: 4px 24px;
  text-decoration: none;
  text-transform: capitalize;
}
.user {
  display: inline-block;
  position: absolute;
  right: 20px;
}
</style>
