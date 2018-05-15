<template lang="html">
  <div class="teacherpracticecreate-wrap">
    <div class="teacherpracticecreate-content">
      <div class="teacherpracticecreate-basic-info">
        <p style="text-align: left; font-size: 1.1rem; font-weight: bold; padding-bottom: 15px;">练习基本信息</p>
        <div class="teacherpracticecreate-title teacherpracticecreate-input">
          <span>练习名</span>
          <div class="teacherpracticecreate-input-wrap">
            <Input v-model="title" size="large" placeholder="练习名" />
          </div>
        </div>
      </div>
      <div class="float-clear">
      </div>
      <div class="hr-wrap">
        <hr />
      </div>
      <div class="teacherpracticecreate-problems">
        <p style="text-align: left; font-size: 1.1rem; font-weight: bold; padding-bottom: 15px;">题目详情</p>
        <div class="teacherpracticeCreate-list-wrap">
          <PracticeCreateItem v-for="problem in problemList" :problem="problem" />
        </div>
        <div class="teacherpracticecreate-plus" id="plus" style="float: left;">
          <span @click="handleNewProblem" style="color: #19be6b; font-weight: bold; font-size: 1.05rem; cursor: pointer;"><Icon type="plus" />&nbsp;新增</span>
        </div>
        <div class="teacherpracticecreate-minus" id="minus" style="display: none;">
          <span @click="handleCollapse" style="color: #2d8cf0; font-weight: bold; font-size: 1.05rem; float: left; padding-bottom: 10px; cursor: pointer;"><Icon type="minus" />&nbsp;收起</span>
          <div class="teacherpracticecreate-input" style="clear: both; float: left;">
            <span>题目</span>
            <div class="teacherpracticecreate-input-wrap">
              <Input v-model="problem" type="textarea" placeholder="题目" rows="3" />
            </div>
          </div>
          <div class="teacherpracticecreate-choices">
            <ChoiceItem v-for="(choice, index) in choices" :choiceValue="choice.value" :cid="choice.cid" @remove="handleRemove(index)" />
            <div class="teacherpracticecreate-input-wrap" style="float: left;">
              <div style="height: 36px; border: 1px dashed #dddee1; border-radius: 4px; cursor: pointer;" @click="handleNewChoice">
                <p style="text-align: left; color: #80848f; padding: 9px 10px;"><Icon type="plus" />&nbsp;新增一个选项</p>
              </div>
            </div>
            <div class="teacherpracticecreate-correct-choice">
              <span style="padding-right: 5px;">正确选项</span>
              <Select v-model="correctAnswer" style="width: 500px;">
                <Option v-for="choice in choices" :value="choice.value" :key="choice.value">
                  {{choice.value}}
                </Option>
              </Select>
            </div>
            <div class="float-clear">
            </div>
          </div>
          <div class="teacherpracticecreate-button-wrap" style="float:left; padding: 10px 0;">
            <Button type="success" size="large" @click="handleSaveProblem">保存此题</Button>
          </div>
        </div>
      </div>
      <div class="float-clear"></div>
      <div class="hr-wrap">
        <hr />
      </div>
      <div class="teacherpracticecreate-button-wrap" style="float:right; padding: 10px;">
        <Button type="success" size="large">保存此练习</Button>
      </div>
    </div>
  </div>
</template>

<script>
import ChoiceItem from './choiceitem';
import Hub from '../assets/hub.js';
import PracticeCreateItem from './practicecreateitem';
var v;

export default {
  name: 'TeacherPracticeCreate',
  data () {
    return {
      title: '',
      problem: '',
      problemCount: 0,
      choices: [],
      correctAnswer: '',
      problemList: [
        {
          problem: 'test01',
          choices: [
            {
              cid: 0,
              value: "test01"
            }
          ],
          correctAnswer: 'test01'
        }
      ]
    }
  },
  components: {
    'ChoiceItem': ChoiceItem,
    'PracticeCreateItem': PracticeCreateItem
  },
  methods: {
    handleNewChoice: function () {
      this.choices.push({cid: this.problemCount, value: '', correct: false});
      this.problemCount += 1;
    },
    handleRemove: function (index) {
      this.choices.splice(index, 1);
    },
    handleNewProblem: function () {
      document.getElementById('plus').style.display = "none";
      document.getElementById('minus').style.display = "block";
    },
    handleCollapse: function () {
      document.getElementById('minus').style.display = "none";
      document.getElementById('plus').style.display = "block";
      this.problem = '';
      this.choices = [];
      this.problemCount = 0;
      this.correctAnswer = '';
    },
    handleSaveProblem: function () {
      if (this.problem === '' ) {
        alert("题面不得为空");
        return;
      } else if (this.choices.length === 0) {
        alert("请添加至少一个选项");
        return;
      } else if (this.correctAnswer === '') {
        alert("请为题目选择正确选项");
        return;
      }
      document.getElementById('minus').style.display = "none";
      document.getElementById('plus').style.display = "block";
      var d = {
        problem: this.problem,
        choices: this.choices,
        correctAnswer: this.correctAnswer
      };
      this.problemList.push(d);
      this.problem = '';
      this.choices = [];
      this.problemCount = 0;
      this.correctAnswer = '';
      console.log(this.problemList);
    }
  },
  created () {
    v = this;

    Hub.$on('SetChoice', function(data) {
      var id = data.index;
      var val = data.value;
      var len = v.choices.length
      for (var i = 0; i < len; i++) {
        if (v.choices[i].cid === id) {
          v.choices[i].value = val;
          return;
        }
      }
    })
  }
}
</script>

<style lang="css">
.float-clear {
  clear: both;
}
.hr-wrap {
  padding: 5px;
}
hr {
  height: 1px;
  border: none;
  border-bottom: 1px solid #dddee1;
}
.teacherpracticecreate-wrap {
  width: 875px;
  height: 100%;
  background-color: #f8f8f9;
  padding: 0 10px;
  float: right;
}
.teacherpracticecreate-content {
  height: 100%;
  overflow-y: auto;
  background-color: #fff;
}
.teacherpracticecreate-basic-info, .teacherpracticecreate-problems {
  padding: 20px 25px 10px;
  float: left;
}
.teacherpracticecreate-input-wrap {
  display: inline-block;
  width: 700px;
  padding-bottom: 5px;
}
.teacherpracticecreate-input>span {
  font-size: 1.1rem;
  padding-right: 5px;
}
.teacherpracticecreate-choices, .teacherpracticecreate-correct-choice {
  float: left;
  padding-top: 10px;
  clear: both;
  width: 100%;
}
</style>
