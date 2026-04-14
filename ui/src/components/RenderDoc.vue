<template>
  <component :is="rendered"/>
</template>

<script setup>
import { computed, h, Fragment } from 'vue'

const { contents } = defineProps(['contents']);
const rendered = computed(() => {
  const e = [];
  let current = [];
  contents.forEach((v) => {

    if(typeof(v.insert) == 'string') {
      // single blank line, styles apply to entire line
      if(v.insert == '\n' && v.attributes) {
        if(v.attributes.header) {
          e.push(h(`h${v.attributes.header}`, {}, current));
        }
        else if(v.attributes.list) {
          e.push(h('li', {}, current));
        }
        else {
          e.push(h('p', {}, current));
        }
        if(v.attributes.indent) {
          e[e.length-1].props['data-indent'] = v.attributes.indent;
        }
        current = [];
        return;
      }

      // one or more lines, probably unformatted,
      // or a fragment with formatting.
      eachLineOf(v.insert, v.attributes, e, current);

    } else if(v.insert.image) {
      
      if(typeof(v.insert.image) == 'string') {
        e.push(h('img', { src: v.insert.image })); 
      } else {
        e.push(h('img', v.insert.image )); 
      }
    }
  });
  return h('div', e);
});

function eachLineOf(text, attrs, e, current) {

  let start = 0;
  while(true) {
    const lf = text.indexOf('\n', start);
    const end = lf == -1 ? text.length : lf;

    const str = text.substring(start, end);

    if(lf == -1) {
      let node = str;
      if(attrs) {
        if(attrs.bold) {
          node = h('strong', [node]);
        }
        if(attrs.italic) {
          node = h('em', [node]);
        }
        if(attrs.underline) {
          node = h('u', [node]);
        }
        if(attrs.link) {
          node = h('a', { href: attrs.link }, [node]);
        }
      }

      current.push(node);
      break;
    }

    e.push(h('p', current.concat(str, h('br'))));
    current.splice(0, current.length);
    start = lf + 1;
  }
}

</script>

<style scoped>
p, h1, h2, h3, h4, h5, h6 {
  margin: 0;
}
[data-indent] {
  padding-left: 48px;
}
img {
  max-width: 100%;
  margin-top: 30px !important;
}
li {
  list-style: inside;
  padding-left: 24px;
}
</style>
