<template lang="html">
  <div class="teachercourselist-wrap">
    <div class="teachercourselist-content">
      <div class="teachercourselist-item teachercourselist-item-first">
        <div class="teachercourselist-course-title">
          <p>Android 应用开发工程师职业规划</p>
        </div>
        <div class="teachercourselist-course-info">
          <p>4 主题 / 23 小节 / 40 练习</p>
        </div>
        <div class="teachercourselist-course-info">
          <p>32 学生参与课程</p>
        </div>
        <div class="teachercourselist-button-group">
          <Button type="primary">编辑课程</Button>
          <Button type="primary">查看学习情况</Button>
        </div>
        <div class="float-clear">
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
  name: 'TeacherCourseList'
}
</script>

<style lang="css">
.teachercourselist-wrap {
  width: 875px;
  float: right;
  height: 100%;
  background-color: #f8f8f9;
  padding: 0 10px;
}
.teachercourselist-content {
  background-color: #fff;
  height: 100%;
  /* padding: 5px 25px; */
}
.teachercourselist-item {
  padding: 5px 25px;
}
.teachercourselist-item-first {
  padding-top: 15px;
}
.teachercourselist-item-last {
  padding-bottom: 20px;
}
.teachercourselist-course-title>p {
  white-space: pre-wrap;
  font-size: 1.5rem;
  text-align: left;
  padding-bottom: 5px;
}
.teachercourselist-course-info>p {
  white-space: pre-wrap;
  text-align: left;
  color: #80848f;
  padding-bottom: 5px;
}
.teachercourselist-button-group {
  float: left;
}
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

</style>
