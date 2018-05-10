<template lang="html">
  <div class="student-course-list">
    <div class="student-course-item">
      <div class="student-course-item-content item-first">
        <div class="course-title">
          <p>Android 应用开发工程师职业规划</p>
        </div>
        <div class="course-description">
          <p>本课程主要向大家介绍 Android 应用开发工程师的职业背景、行业前景、团队中的定位及所需的技能，同时分享 Android 应用开发的学习方法和路径以及将来的职业规划</p>
        </div>
        <div class="course-info">
          <div class="teacher-info">
            <div class="avatar">
              <Avatar icon="person" size="small" />
            </div>
            <div class="teacher-name">
              <p>老师 A</p>
            </div>
          </div>
          <div class="last-progress">
            <p>上次学到&nbsp;&nbsp;&nbsp;<span class="last-progress-section">Android 应用开发工程师职业规划</span></p>
          </div>
          <div class="float-clear">
          </div>
        </div>
      </div>
      <div class="hr-wrap">
        <hr />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentCourseList',
  data () {
    return {

    }
  }
}
</script>

<style lang="css">
.hr-wrap {
  padding: 5px;
}
hr {
  height: 1px;
  border: none;
  border-bottom: 1px solid #dddee1;
}

.student-course-list {
  float: right;
  width: 860px;
  height: 100%;
  background-color: #ffffff;
}
.student-course-item-content {
  padding: 5px 25px;
}
.item-first {
  padding-top: 20px;
}
.item-last {
  padding-bottom: 20px;
}

.course-title {
  padding-bottom: 5px;
}
.course-title>p {
  color: #495060;
  font-size: 1.5rem;
  text-align: left;
}

.course-description{
  padding-bottom: 10px;
}
.course-description>p {
  color: #80848f;
  text-align: left;
}

.teacher-info {
  float: left;
}
.teacher-name {
  display: inline-block;
  padding: 0 5px;
}
.teacher-info>p {
  color: #80848f;
  text-align: left;
}

.last-progress {
  float: right;
}
.last-progress>p {
  text-align: right;
}
.last-progress-section {
  color: #2d8cf0;
  font-weight: bold;
}

</style>
