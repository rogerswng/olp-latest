<template lang="html">
  <div class="problem-wrap">
    <div class="problem-content">
      <p>在 C++ 中使用流进行输入输出，其中用于屏幕输出的对象是（  ）</p>
    </div>
    <div class="problem-choices-wrap">
      <Choice choiceid="1" choiceclass="choice-content" @choiceselected="listenToSelected" />
      <Choice choiceid="2" choiceclass="choice-content" @choiceselected="listenToSelected" />
      <Choice choiceid="3" choiceclass="choice-content" @choiceselected="listenToSelected" />
      <Choice choiceid="4" choiceclass="choice-content" @choiceselected="listenToSelected" />
    </div>
    <div class="problem-op-wrap">
      <div class="problem-button-wrap">
        <Button type="error" size="large">交卷</Button>
      </div>
      <div class="problem-button-wrap">
        <Button type="primary" size="large">下一题</Button>
      </div>
      <div class="float-clear">
      </div>
    </div>
  </div>
</template>

<script>
import Choice from './choice';

export default {
  name: 'Problem',
  data () {
    return {
      selectedValue: ''
    }
  },
  components: {
    'Choice': Choice
  },
  methods: {
    listenToSelected: function (op) {
      if (op["status"] === 1) {
        // Handle with clearing THE choice
        // console.log(op["choiceid"]);
        choiceid = op["choiceid"];
        this.selectedValue = '';
      } else {
        // Handle with select THE choice
        // console.log(op["choiceid"]);
        var choiceid = op["choiceid"];
        this.selectedValue = choiceid;
        var eleList = document.getElementsByClassName('choice-content');
        var eleCount = eleList.length;
        for (var i = 0; i < eleCount; i++) {
          if (eleList[i].id === choiceid) {
            eleList[i].className = "choice-content choice-content-active";
          } else {
            eleList[i].className = "choice-content";
          }
        }
      }
    }
  }
}
</script>

<style lang="css">
.problem-wrap {
  background-color: #fff;
  padding: 15px 20px;
}
.problem-content {
  padding-bottom: 20px;
}
.problem-content>p {
  text-align: left;
  font-size: 1.1rem;
  white-space: pre-wrap;
  color: #1c2438;
  padding: 0 10px;
}
.problem-button-wrap {
  float: right;
  padding-left: 10px;
}
</style>
