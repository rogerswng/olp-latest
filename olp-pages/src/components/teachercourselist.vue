<template lang="html">
  <div class="teachercourselist-wrap">
    <div class="teachercourselist-content">
      <div style="padding: 5px 0;">
      </div>
      <div v-for="course in courses" class="teachercourselist-item-wrap">
        <div class="teachercourselist-item">
          <div class="teachercourselist-course-title">
            <p><router-link :to="{ name: 'TeacherCourseEdit', params: {id: course.id}}"><span>{{course.title}}</span></router-link></p>
          </div>
          <div class="teachercourselist-course-info">
            <p>{{course.info}}</p>
          </div>
          <div class="teachercourselist-course-info">
            <p>{{course.students}} 学生参与课程</p>
          </div>
          <div class="teachercourselist-button-group">
            <router-link :to="{ name: 'TeacherCourseEdit', params: {id: course.id} }"><Button type="primary">编辑课程</Button></router-link>
            <router-link :to="{ name: 'ImportStudent', params: {courseid: course.id} }"><Button type="primary" @click="handleImportStudent">导入学生</Button></router-link>
            <!-- <Button type="error" @click="handleRemove">下线课程</Button> -->
          </div>
          <div class="float-clear">
          </div>
        </div>
        <div class="hr-wrap">
          <hr />
        </div>
      </div>
      <!-- <div class="teachercourselist-item teachercourselist-item-first">
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
      </div> -->
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TeacherCourseList',
  data () {
    return {
      courses: []
      // courses: [
      //   {
      //     id: '123t64192301',
      //     title: 'Android 应用开发工程师职业规划',
      //     info: '4 主题 / 23 小节 / 40 练习',
      //     students: 32
      //   }
      // ]
    }
  },
  methods: {
    handleImportStudent: function () {
      console.log("handle import student");
    },
    handleRemove: function () {
      console.log("handle remove");
    },
    initComp: function () {
      var userId = this.$getCookie("uid");
      axios.get("http://"+this.BASEURL+"/teacherCourseList?userId="+userId).then(function(res) {
        // console.log(res);
        var c = res.data.courses;
        console.log(c);
        for (var i = 0; i < c.length; i++) {
          c[i].students = c[i].count[3];
          c[i].info = c[i].count[0]+" Topics / "+c[i].count[1]+" Sections / "+c[i].count[2]+" Practices";
        }
        this.courses = c;
      }.bind(this));
    }
  },
  mounted () {
    this.initComp();
  }
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
