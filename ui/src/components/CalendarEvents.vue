<template>
  <div class="calendar">

    <div class="view">
      <button :disabled="listView" @click="listView = true"> <fa icon="fa-clipboard-list"/> </button>
      <button :disabled="!listView" @click="listView = false"> <fa icon="fa-regular fa-calendar-days"/> </button>
    </div>

    Upcoming events:
    <div class="list" v-if="listView">

      <div class="event" v-for="event in upcomingEvents">
        <div class="start">
          {{ event.startDate }} - {{ event.startTime }}
          <a class="attachment" :href="event.fields.attach" target="_blank" v-if="event.fields.attach">
            <fa icon="fa-paperclip"/> Attachment
          </a>
        </div>
        <div class="summary">
          {{ event.fields.summary }}
        </div>
      </div>
    </div>
    <div class="month" v-else>
      <div class="name"> {{ month }} </div>
      <div class="day" v-for="day in days" :data-dow="day.dayOfWeek" :class="{ current: day.current, today: day.today, past: day.past }">
        <div class="date"> {{ day.date }} </div>
        <div class="event" v-for="event in eventListForDate(day.month, day.date)">
          {{ event.startTime }}
          {{ event.fields.summary }}
          <a class="attachment" :href="event.fields.attach" target="_blank">
            <fa icon="fa-paperclip" v-if="event.fields.attach"/>
          </a>
        </div>
      </div> 
    </div>

    Subscribe:
    <input class="link" @click.prevent="$event.target.select()" readonly value="https://foxmarchingwarriors.band/calendar.ics">
      <!--fa icon="fa-regular fa-clone"/-->
    </input>

    <div class="edit" v-if="user && user.scopes.includes('edit')">
      <p>
        For updating:
        <a :href="calendarUrl" target="_blank"> Open in Google Calendar <fa icon="fa-external-link"/></a>
      </p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ICAL from 'ical.js'
import { useAuth } from '@/components/Auth'

const auth = useAuth();
const user = ref(auth.getAuthInfo());

const listView = ref(true);
const upcomingEvents = ref([]);
const monthEvents = ref({});

const month = ref();
const days = ref([]);
const byDate = ref({});
const calendarUrl = ref(process.env.VUE_APP_CALENDAR_URL);

function currentMonthName(start) {
  return (start).toLocaleString('default', {month: 'long'});
}

function currentMonthDays(start) {
  const d = new Date(start);
  const w = d.getDay();

  d.setMonth(d.getMonth() + 1);
  d.setDate(0);
  const last = d.getDate();

  const calendar = [];
  const today = new Date();

  for(let i = 1; i <= 35; ++i) {
    const day = {
      dayOfWeek: ((i-1)%7) + 1,
    };

    if(i <= w) {
      const n = new Date(start);
      n.setDate(0);
      day['date'] = n.getDate() - (w-i);
      day['month'] = n.getMonth() + 1;

      if(n.getMonth() == today.getMonth() && n.getDate() - (w-i) == today.getDate()) {
        day['today'] = true;
      }
    } else if (i <= last + w) {
      day['month'] = d.getMonth() + 1;
      day['date'] = i - w;
      day['current'] = true;

      if(d.getMonth() == today.getMonth() && (i - w) == today.getDate()) {
        day['today'] = true;
      }
    } else {
      const n = new Date(start);
      n.setMonth(start.getMonth() + 1);
      n.setDate(i - w - last);
      day['date'] = n.getDate();
      day['month'] = n.getMonth() + 1;
    }

    if((start.getMonth() < today.getMonth() || start.getMonth() == today.getMonth()) && (i - w) < today.getDate()) {
      day['past'] = true;
    }

    calendar.push(day);
  }
  return calendar;
}

function eventListForDate(m, d) {
  const list = monthEvents.value[m + "-" + d];
  if(list) {
    return list;
  }
}

const startDate = new Date();
startDate.setDate(1);
days.value = currentMonthDays(startDate);
month.value = currentMonthName(startDate);
if(days.value.findIndex((d) => d.date == new Date().getDate()) / 7 >= 4) {
  startDate.setMonth(startDate.getMonth() + 1);
  days.value = currentMonthDays(startDate);
  month.value = currentMonthName(startDate);
}

onMounted(async () => {
  const response = await fetch('/api/events/2026-04-01/2026-12-31');
  const today = new Date();
  today.setHours(23);
  today.setMinutes(59);
  if(response.ok) {
    (await response.json()).events.forEach((e) => {
      const d = new Date(e.start);

      const data = ICAL.parse(e.data);
      const fields = data[1].reduce((h, v, i) => {
        h[v[0]] = v[3];
        return h;
      }, {});

      const info = {
        startDate: d.toDateString(),
        startTime: d.toLocaleTimeString(),
        fields: fields,
      };


      if(upcomingEvents.value.length < 5 && d > today) {
        upcomingEvents.value.push(info);
      }

      (monthEvents.value[(d.getMonth() + 1) + "-" + d.getDate()] ||= []).push(info);
    });
  }
});

</script>

<style scoped>
.calendar {
  padding: 40px 0;
  position: relative;
}

.view {
  position: absolute;
  right: 0;
}

.view button {
  background: none;
  border: none;
  color: grey;
  margin-left: 24px;
  cursor: pointer;
}

.view button:disabled {
  color: black;
  border-bottom: 1px solid black; 
  cursor: default;
}

.list, .month {
  min-height: 60px;
}

.month {
  margin: 20px 0;
}

.month .name {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
  text-align: center;
}

.day {
  display: inline-block;
  width: 13.5%;
  height: 120px;
  border: 1px solid #aaa;
  margin: 1px;
  vertical-align: top;
}
.day[data-dow="1"], .day[data-dow="7"] {
  background: #eee;
}

.day:not(.current) {
  background: #ddd;
}
.day[data-dow="1"]:not(.current), .day[data-dow="7"]:not(.current) {
  background: #ccc;
}

.day.today {
  border: 1px solid red;
}

.event {
  background: grey;
  color: white;
  border-radius: 8px;
  position: relative;
}

.event .attachment {
  color: white;
  font-weight: bold;
  text-decoration: none;
  display: block;
  padding: 8px 0 16px 0;
}

.day.past .event {
  opacity: 0.5; 
}

.month .event {
  font-size: 12px;
  padding: 2px 4px;
  margin: 1px 2px;
  height: 36px;
}

.list .event {
  margin: 20px 0;
  padding: 8px 20px;
}
.list .event:last-of-type {
  margin-bottom: 40px;
}

.link {
  display: block;
  font-family: mono;
  font-size: 14px;
  padding: 2px;
  background: #eee;
  border: 1px solid #aaa;
  text-align: center;
  width: 100%;
}

.link svg {
  margin-left: 8px;
}
@media screen and (min-width: 425px) {
  .link {
    width: 22em;
  }
}

@media screen and (min-width: 768px) {
  .link {
    display: inline-block;
    margin-left: 32px;
    font-size: 16px;
  }
  .list .event .attachment {
    display: inline;
    float: right;
  }
}
</style>
