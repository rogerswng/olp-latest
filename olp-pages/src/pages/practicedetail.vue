<template lang="html">
  <div class="practicedetail-main">
    <Header />
    <div class="practicedetail-content-wrap">
      <div class="practicecard-wrap">
        <ProblemCard />
      </div>
      <div class="practice-problem-wrap">
        <Problem />
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../components/header';
import Problem from '../components/problem';
import ProblemCard from '../components/problemcard';

export default {
  name: 'PracticeDetail',
  data () {
    return {

    }
  },
  components: {
    'Header': Header,
    'Problem': Problem,
    'ProblemCard': ProblemCard
  }
}
</script>

<style scoped lang="css">
.practicedetail-main {
  height: 100%;
  background-color: #f8f8f9;
}
.practicedetail-content-wrap {
  width: 1175px;
  margin: 0 auto;
  padding: 10px 0;
}
</style>
