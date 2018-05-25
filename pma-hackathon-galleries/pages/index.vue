<template>
  <div class="app main">
    <header>
      <div class="logo">
        <div class="line"></div>
        <div class="line alt"></div>
        <div class="line alt second"></div>
        <div class="line"></div>
      </div>
      <h1>Tailwind</h1>
    </header>
    <div class="directions">
      <p>Which team do you belong to?</p>
      <ul>
        <li>Adventurer</li>
        <li>Spiritualist</li>
        <li>Scholar</li>
        <li>Creative</li>
      </ul>
    </div>
    <div><a href="questions">Find out</a></div>
  </div>
</template>

<style scoped>
.main {
  background-color: white;
}

h1 {
  text-transform: lowercase;
  display: inline;
  vertical-align: top;
  font-size: 40px;
}

.directions {
  font-size: 2em;
}

.directions p {
  font-size: 1.2em;
  line-height: 1.2em;
}
.directions ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.directions li:nth-child(1) {
  color: #E83A17;
}
.directions li:nth-child(2) {
  color: #C10F8A;
}
.directions li:nth-child(3) {
  color: #79CCB7;
}
.directions li:nth-child(4) {
  color: #FFCB00;
}


.logo {
  padding-right: 20px;
  display: inline-block;
  width: 100px;
  margin: 0 auto;
}

.logo .line {
  background: linear-gradient(to right, #EBBE29 0%,#84BC9D 100%);
  height: 5px;
  width: 60px;
  margin: 10px 0;
}
.logo .line.alt {
  background: linear-gradient(to right, #E83A17 0%,#C10F8A 100%);
  margin-left: 30px;
}
.logo .line.alt.second {
  margin-left: 20px;
}

.main a {
  background-color: #E83A17;
  color: white;
}

.main a:hover {
  background-color: transparent;
  border-color: #E83A17;
  color: #E83A17;
}
</style>