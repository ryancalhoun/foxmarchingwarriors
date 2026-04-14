<template>
  <div class="calendar">
    Upcoming events:

    <div class="event" v-for="event in events">
      <div class="start">
        {{ event.start }}
      </div>
      <div class="summary">
        {{ event.data[1][0][3] }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ICAL from 'ical.js'

const events = ref();
onMounted(async () => {
  const response = await fetch('/api/events');
  if(response.ok) {
    events.value = (await response.json()).events.map((e) => {
      const d = new Date(e.start);
      return {
        start: d.toDateString() + " - " + d.toLocaleTimeString(),
        data: ICAL.parse(e.data),
      }
    });
  }
});

</script>

<style scoped>
.calendar {
  padding: 40px 0;
}

.event {
  margin: 20px 0;
  padding: 8px 20px;
  background: grey;
  color: white;
  border-radius: 8px;
}
</style>
