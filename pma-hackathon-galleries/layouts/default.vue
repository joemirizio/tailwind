<template>
    <nuxt>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-119873309-1"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'UA-119873309-1');
    </script>
    </nuxt>
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