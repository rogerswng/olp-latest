<template lang="html">
  <div class="teacherpracticecreate-item">
    <div class="problem-label">
      <p>{{p}}</p>
    </div>
    <div class="choices">
      <p v-for="choice in choices">{{choice.value}}<span class="correct-answer" v-if="choice.value === correctAnswer">(正确答案)</span>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PracticeCreateItem',
  data () {
    return {
      p: this.problem.problem,
      choices: this.problem.choices,
      correctAnswer: this.problem.correctAnswer
    }
  },
  props: ['problem'],
  mounted () {

  }
}
</script>

<style lang="css">
.teacherpracticecreate-item {
  padding-bottom: 15px;
}
.problem-label>p, .choices>p {
  text-align: left;
  white-space: pre-wrap;
}
span.correct-answer {
  color: #19be6b;
}
</style>
