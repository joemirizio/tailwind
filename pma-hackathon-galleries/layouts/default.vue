<template>
  <nuxt/>
</template>

<script>
  export default {
    data() {
      return { 'title': 'Tailwind' }
    },
    head() {
      return {
        title: this.title,
        meta: [
          { hid: 'viewport', name: 'viewport', content: 'width=device-width, initial-scale=1, shrink-to-fit=no' }
        ],
        link: [
          { href: 'https://fonts.googleapis.com/css?family=Titillium+Web:300,400,700', rel: 'stylesheet' }
        ]
      }
    }
  }
</script>