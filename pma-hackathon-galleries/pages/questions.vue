<template>
<div class="app questions">
  <div><button @click="chooseA">{{ choiceA() }}</button></div>
  <hr />
  <p>or</p>
  <hr />
  <div><button @click="chooseB">{{ choiceB() }}</button></div>
</div>
</template>

<script>
import questions from '~/assets/questions.json';
const SCHOLAR = 0;
const CREATIVE = 1;
const ADVENTURER = 2;
const SPIRITUALIST = 3;

export default {
  data() {
    return { 
      question: 0,
      scores: [0, 0, 0, 0]
    };
  },
  methods: {
    choiceA() {
      return questions[this.question][0];
    },
    choiceB() {
      return questions[this.question][1];
    },
    chooseA() {
      this.calculateScore(0);
    },
    chooseB() {
      this.calculateScore(1);
    },
    calculateScore(i) {
      switch (this.question) {
        case 0:
        case 1:
          this.scores[this.question + i] = 1;
          break;
        case 2:
        case 3:
          this.givePoints(SCHOLAR, ADVENTURER, i);
          break;
        case 4:
        case 5:
          this.givePoints(SCHOLAR, SPIRITUALIST, i);
          break;
        case 6:
        case 7:
          this.givePoints(CREATIVE, ADVENTURER, i);
          break;
        case 8:
        case 9:
          this.givePoints(CREATIVE, SPIRITUALIST, i);
          break;
      }
      this.nextQuestion();
    },
    nextQuestion() {
      if (this.question === 1) {
        if (this.scores[SCHOLAR] && this.scores[ADVENTURER]) {
          this.question = 2;
        } else if (this.scores[SCHOLAR] && this.scores[SPIRITUALIST]) {
          this.question = 4;
        } else if (this.scores[CREATIVE] && this.scores[ADVENTURER]) {
          this.question = 6;
        } else {
          this.question = 8;
        }
      } else if (this.question % 2 === 1) {
        const team = this.determineTeam();
        window.location = `result/${team}`
      } else {
        this.question++;
      }
    },
    givePoints(a, b, i) {
      this.scores[(i == 0 ? a : b)]++;
    },
    determineTeam() {
      // https://stackoverflow.com/questions/11301438/return-index-of-greatest-value-in-an-array#11301464
      return this.scores.reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0);
    }
  }
};
</script>

<style scoped>
.questions button:hover {
  background-color: white;
  color: #C10F8A;
}

.questions hr {
  flex: 1;
  border: 2px solid #FFCB00;
}

.questions {
  background-color: #C10F8A;
  color: white;
}
</style>