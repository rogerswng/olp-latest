<template lang="html">
  <div class="practicedetail-main">
    <Header />
    <div class="practicedetail-content-wrap">
      <div class="practicecard-wrap">
        <ProblemCard :problemcount="problemCount" @change="handleProblemChange" :curproblem="curProblemIndex" />
      </div>
      <div class="practice-problem-wrap">
        <Problem v-for="(problem, index) in problems" :id="'p'+index" :problemid="index" :p="problem" @remove="handleRemove" @choose="handleChoose" style="display: none;"/>
      </div>
      <div class="problem-op-wrap">
        <div class="problem-button-wrap" v-if="submit != 2">
          <Button type="error" size="large" @click="handleSubmit">交卷</Button>
        </div>
        <div class="problem-button-wrap">
          <router-link :to="{path:'/studentmain/practice'}"><Button type="error" size="large">返回练习列表</Button></router-link>
        </div>
        <div class="problem-button-wrap" v-if="curProblemIndex+1 != problemCount">
          <Button type="primary" size="large" @click="handleNext">下一题</Button>
        </div>
        <div class="problem-button-wrap" v-else>
          <Button type="primary" size="large" @click="handlePrevious">上一题</Button>
        </div>
        <div class="float-clear">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../components/header';
import Problem from '../components/problem';
import ProblemCard from '../components/problemcard';
import axios from 'axios';

export default {
  name: 'PracticeDetail',
  data () {
    return {
      practiceId: this.$route.params.id,
      problems: [
        // {
        //   id: '1235452137123',
        //   content: '在 C++ 中使用流进行输入输出，其中用于屏幕输出的对象是（  ）',
        //   choices: [
        //     '这是第一个选项 cerrrrrr',
        //     'cerr', 'cout', 'cin'
        //   ],
        //   status: 0
        // },
        // {
        //   id: '123557238239',
        //   content: '这是第二个题目，测试测试测试题（  ）',
        //   choices: [
        //     'ttttttt010101', 'tueyweyr1', 'ushsfshda', 'asdufgadjczcbcz', 'adusfgidhasd', '12easdasfxz'
        //   ],
        //   status: 1,
        //   draft: 1
        // },
        // {
        //   id: '1236123981294',
        //   content: '这个题目有问题（  ）',
        //   choices: [
        //     'sadfjhuwyieh', 'afkhw udyahsd', 'asufhufyahdosd'
        //   ],
        //   status: 2,
        //   draft: 0,
        //   correctAnswer: 1
        // },
        // {
        //   id: '27ywt734612943',
        //   content: '这个题目有问题2（ ）',
        //   choices: [
        //     'asdjfhqu', 'sfkjhssakd', 'afhiquwd', 'afusgfsd'
        //   ],
        //   status: 2,
        //   draft: 1,
        //   correctAnswer: 1
        // }
      ],
      curProblemIndex: 0,
      problemCount: 0,
      submit: 0
    }
  },
  components: {
    'Header': Header,
    'Problem': Problem,
    'ProblemCard': ProblemCard
  },
  methods: {
    handleRemove: function (d) {
      this.problems[d.index].status = 0;
      this.problems[d.index].draft = '';
    },
    handleChoose: function (d) {
      this.problems[d.index].status = 1;
      this.problems[d.index].draft = this.problems[d.index].choices.indexOf(d.val);
      this.problems[d.index].selected = d.val;
    },
    handleSubmit: function () {
      console.log(this.problems);
      for (var i = 0; i < this.problems.length; i++) {
        if (this.problems[i].status === 0) {
          alert("还有空白题目，请返回检查！");
          return;
        }
      }
      var d = {
        uid: this.$getCookie("uid"),
        practiceId: this.$route.params.id,
        problems: this.problems
      }
      axios.post("http://"+this.BASEURL+"/markPractice",d).then(function(res) {
        console.log(res);
        this.problems = res.data;
        this.submit = 2;
      }.bind(this));
    },
    handleNext: function () {
      this.curProblemIndex += 1;
    },
    handlePrevious: function () {
      this.curProblemIndex -= 1;
    },
    handleProblemChange: function (d) {
      var nxtid = d.next;
      this.curProblemIndex = nxtid;
    }
  },
  mounted () {
    axios.get("http://"+this.BASEURL+"/fetchProblems?practiceId="+this.$route.params.id+"&uid="+this.$getCookie("uid")).then(function(res) {
      console.log(res);
      this.problems = res.data.problemSet;
      this.problemCount = res.data.problemSet.length;
      this.submit = res.data.status;
    }.bind(this));
  },
  beforeDestroy () {
    // console.log("destroy");
    // alert("Here!");
    if (this.submit === 2) {
      return;
    } else {
      var d = {
        uid: this.$getCookie("uid"),
        practiceId: this.practiceId,
        problems: this.problems
      }
      console.log(d.practiceId);
      axios.post("http://"+this.BASEURL+"/savePracticeDraft",d).then(function(res) {
        if (res.data.success) {
          alert("Saved!");
        }
      })
    }
  },
  watch: {
    curProblemIndex: function (cur) {
      var curid = "pc"+cur;
      var pid = "p"+cur;
      console.log(curid);
      var eles = document.getElementById('practicecard').children;
      for (var i = 0; i < eles.length; i++) {
        if (eles[i].id === curid) {
          document.getElementById(eles[i].id).className = 'problemcard-nav problemcard-cur';
          document.getElementById(pid).style.display = "block";
        } else {
          document.getElementById(eles[i].id).className = 'problemcard-nav';
          document.getElementById('p'+i).style.display = 'none';
        }
      }
    }
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
  background-color: #f8f8f9;
  /* height: 600px; */
  /* overflow-y: auto; */
}
.problem-button-wrap {
  float: right;
  padding-left: 10px;
  padding-top: 10px;
}
</style>
