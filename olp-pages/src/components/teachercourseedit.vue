<template lang="html">
  <div class="teachercourseedit-wrap">
    <div class="teachercourseedit-content">
      <div style="padding: 10px;">
      </div>
      <CourseEditItem v-for="course in courseDetail" :course="course" @removetopic="handleRemoveTopic" @removesection="handleRemoveSection"/>
    </div>
  </div>
</template>

<script>
import CourseEditItem from './courseedititem.vue';

export default {
  name: 'TeacherCourseEdit',
  data () {
    return {
      courseDetail: [
        {
          id: "0",
          topicTitle: 'TestTitle01',
          sections: [
            {
              id: "0",
              sectionTitle: 'SectionTitle01',
              entityType: 'video'
            },
            {
              id: "1",
              sectionTitle: 'SectionTitle02',
              entityType: 'doc',
              content: 'blah'
            }
          ]
        }
      ]
    }
  },
  components: {
    'CourseEditItem': CourseEditItem
  },
  methods: {
    handleRemoveTopic: function (index) {
      for (var i = 0; i < this.courseDetail.length; i++) {
        if (this.courseDetail[i].id === index) {
          if (confirm("确定要删除？")) {
            this.courseDetail.splice(i, 1);
            return;
          }
        }
      }
    },
    handleRemoveSection: function (index) {
      var s;
      console.log("Here!");
      for (var i = 0; i < this.courseDetail.length; i++) {
        s = this.courseDetail[i].sections;
        console.log(s);
        for (var j = 0; j < s.length; j++) {

          if (s[j].id === index) {
            if (confirm("确定要删除？")) {
              this.courseDetail[i].sections.splice(j, 1);
              console.log(this.courseDetail);
              return;
            }
          }
        }
      }
    }
  }
}
</script>

<style lang="css">
.teachercourseedit-wrap {
  height: 100%;
  background-color: #f8f8f9;
  width: 875px;
  padding: 0 10px;
  float: right;
}
.teachercourseedit-content {
  height: 100%;
  background-color: #fff;
}
.teachercourseedit-list-item {
  padding: 5px 25px;
}
.topictitle-label {
  padding-bottom: 5px;
}
.topictitle-label>p, .section-list>p {
  text-align: left;
  white-space: pre-wrap;
}
.topictitle-label>p {
  font-weight: bold;
  font-size: 1.1rem;
}
.section-list>p {
  font-size: 1rem;
  padding-top: 5px;
}
.span-edit {
  color: #2d8cf0;
  cursor: pointer;
}
.span-remove {
  color: #ed3f14;
  cursor: pointer;
}
.span-open, .span-close {
  cursor: pointer;
}
</style>
