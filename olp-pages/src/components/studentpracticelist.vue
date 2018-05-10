<template lang="html">
  <div class="list-wrap student-practice-list">
    <div class="student-practice-item">
      <div class="student-practice-item-content item-first">
        <div class="practice-title">
          <p>课后练习</p>
        </div>
        <div class="practice-relation">
          <p>Android 应用工程师职业规划 / Android 应用工程师职业规划 / Android 应用工程师职业规划</p>
        </div>
        <div class="practice-info">
          <p>36 人完成 · 平均 90 分 · 平均用时 12 分钟</p>
        </div>
      </div>
      <div class="practice-status item-first">
        <Button type="primary">去完成</Button>
      </div>
      <div class="float-clear">
      </div>
      <div class="hr-wrap">
        <hr />
      </div>
    </div>
    <div class="student-practice-item">
      <div class="student-practice-item-content item-first">
        <div class="practice-title">
          <p>课后练习</p>
        </div>
        <div class="practice-relation">
          <p>Android 应用工程师职业规划 / Android 应用工程师职业规划 / Android 应用工程师职业规划</p>
        </div>
        <div class="practice-info">
          <p>36 人完成 · 平均 90 分 · 平均用时 12 分钟 · <span class="my-score">我的成绩 90 分</span></p>
        </div>
      </div>
      <div class="practice-status item-first">
        <p>已完成</p>
      </div>
      <div class="float-clear">
      </div>
      <div class="hr-wrap">
        <hr />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentPracticeList',
  data () {
    return {

    }
  }
}
</script>

<style lang="css">
hr {
  height: 1px;
  border: none;
  border-bottom: 1px solid #dddee1;
}
.hr-wrap {
  padding: 5px;
}

.student-practice-list {
  float: right;
  width: 860px;
  height: 100%;
  background-color: #ffffff;
}

.student-practice-item {
  position: relative;
}

.student-practice-item-content {
  padding: 5px 25px;
  width: 700px;
  float:left;
}
.item-first {
  padding-top: 20px;
}
.item-last {
  padding-bottom: 20px;
}

.practice-title {
  padding-bottom: 5px;
}
.practice-title>p {
  color: #495060;
  font-size: 1.5rem;
  text-align: left;
}

.practice-relation {
  padding-bottom: 10px;
}
.practice-relation>p {
  color: #80848f;
  text-align: left;
}

.practice-info>p {
  text-align: left;
}
.my-score {
  color: #268cf0;
  font-weight: bold;
}

.practice-status {
  position: absolute;
  right: 0;
  top: 50%;
  height: 52px;
  transform: translateY(-36px);
  width: 160px;
}
.practice-status>p {
  color: #2d8cf0;
  font-size: 0.8rem;
  font-weight: bold;
  line-height: 32px;
}


</style>
