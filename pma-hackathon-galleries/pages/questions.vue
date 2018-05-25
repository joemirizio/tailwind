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
      scores: [0, 0, 0, 0],
      isSwitched: false
    };
  },
  methods: {
    choiceA() {
      return questions[this.question][this.actualChoice(0)];
    },
    choiceB() {
      return questions[this.question][this.actualChoice(1)];
    },
    chooseA() {
      this.calculateScore(this.actualChoice(0));
    },
    chooseB() {
      this.calculateScore(this.actualChoice(1));
    },
    actualChoice(index) {
      return !this.isSwitched ? index : (!index + 0);
    },
    setSwitched() {
      this.isSwitched = (Math.random() >= 0.5);
    },
    calculateScore(i) {
      switch (this.question) {
        case 0:
        case 1:
          this.scores[this.question * 2 + i] = 1;
          break;
        case 2:
        case 3:
        case 4:
          this.givePoints(SCHOLAR, ADVENTURER, i);
          break;
        case 5:
        case 6:
        case 7:
          this.givePoints(SCHOLAR, SPIRITUALIST, i);
          break;
        case 8:
        case 9:
        case 10:
          this.givePoints(CREATIVE, ADVENTURER, i);
          break;
        case 11:
        case 12:
        case 13:
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
          this.question = 5;
        } else if (this.scores[CREATIVE] && this.scores[ADVENTURER]) {
          this.question = 8;
        } else {
          this.question = 11;
        }
        this.setSwitched();
      } else if ((this.question - 1) % 3 === 0) {
        const team = this.determineTeam();
        window.location = `result/${team}`
      } else {
        if (this.question > 0) {
          this.setSwitched();
        }
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