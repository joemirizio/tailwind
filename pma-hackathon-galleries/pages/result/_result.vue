<template>
<div class="app result" :style="backgroundImageStyle()">
  <div class="container">
    <h2>You're an art</h2>
    <h1>{{ name() }}</h1>
    <p class="info">{{ description() }}</p>
    <div class="buttons">
      <a class="primary" :href="`https://twitter.com/home?status=${twitterStatus()}`">Share</a>
      <a href="/">Back</a>
    </div>
  </div>
</div>
</template>

<script>
  import teams from '~/assets/teams.json';

  export default {
    asyncData (context) {
      return { team: context.params.result };
    },
    validate ({ params }) {
      return (params.result >= 0 && params.result < teams.length);
    },
    methods: {
      name() {
        return teams[this.team].name;
      },
      pronoun() {
        return (this.name() === 'Adventurer') ? 'an' : 'a';
      },
      description() {
        return teams[this.team].description;
      },
      backgroundImageStyle() {
        return {
          backgroundImage: `url(${teams[this.team].image})`
        };
      },
      twitterStatus() {
        return encodeURI(`Tailwind says I'm ${this.pronoun()} "${this.name()}"! See what you are at http://museumcrawlers.com`)
      }
    }
  };
</script>

<style scoped>
.result {
  background-size: cover;
}
.result::after {
  background-color: rgba(121, 204, 183, 0.5);
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}

.result .container {
  background-color: #79ccb7;
  display: flex;
  flex-direction: column;
  position: relative;
  flex: 1;
  z-index: 1;
  padding: 20px;
}

.result .container::after {
  position: absolute;
  top: 70px;
  height: 50px;
  left: 0;
  width: 50px;
  content: '';
  background-color: #C10F8A;
}
.result .info {
  flex: 1;
}

.result .buttons {
  height: 50px;
}

.result a {
  color: black;
  border-color: black;
}
.result a:hover {
  color: #79ccb7;
  background-color: black;
}
.result a.primary {
  color: #79ccb7;
  background-color: black;
}

.result a.primary:hover {
  color: black;
  background-color: transparent;
}
</style>