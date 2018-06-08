<template lang="html">
  <div class="practice-main">
    <Header />
    <div class="content-wrap">
      <div class="practice-content">
        <div class="practice-detail-title">
          <p>{{ title }}</p>
        </div>
        <div class="practice-detail-relation">
          <p>{{ relation }}</p>
        </div>
        <div class="practice-detail-info">
          <p>{{ info }}</p>
        </div>
        <div class="practice-button-wrap">
          <router-link :to="{ name: 'PracticeDetail', params: {id: id} }"><Button type="primary">开始练习</Button></router-link>
          <div class="float-clear">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../components/header';
import axios from 'axios';

export default {
  name: 'Practice',
  data () {
    return {
      id: '',
      title: '',
      relation: '',
      info: ''
    }
  },
  created () {
    console.log(this.$route.params);
  },
  mounted () {
    axios.get("http://"+this.BASEURL+"/practiceBasic?practiceId="+this.$route.params.id).then(function(res) {
      console.log(res);
      this.id = res.data.practice_id;
      this.title = res.data.title;
      this.relation = res.data.relation;
    }.bind(this));
  },
  components: {
    'Header': Header
  }
}
</script>

<style scoped lang="css">
.practice-main {
  height: 100%;
  background-color: #f8f8f9;
}
.content-wrap {
  height: 100%;
  background-color: #f8f8f9;
}
.practice-content {
  background-color: #ffffff;
  margin: 10px auto;
  width: 1175px;
  padding-top: 20px;
  padding-bottom: 30px;
  padding: 20px 0 30px 15px;
}

.practice-detail-title {
  padding-bottom: 5px;
}
.practice-detail-title>p {
  text-align: left;
  font-size: 2rem;
  /* font-weight: bold; */
  color: #1c2438;
  white-space: pre-wrap;

}

.practice-detail-relation {
  padding-bottom: 5px;
}
.practice-detail-relation>p {
  text-align: left;
  font-size: 1.1rem;
  color: #80848f;
  white-space: pre-wrap;
}

.practice-detail-info {
  padding-bottom: 10px;
}
.practice-detail-info>p {
  text-align: left;
  white-space: pre-wrap;
}

.practice-button-wrap>a>button {
  float: left;
}
</style>
