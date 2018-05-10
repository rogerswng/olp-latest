<template lang="html">
  <div class="course-main">
    <Header />
    <div class="content-wrap">
      <div class="course-content">
        <CourseInfo />
        <CourseOutline />
        <div class="float-clear">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../components/header';
import CourseInfo from '../components/courseinfo';
import CourseOutline from '../components/courseoutline';

export default {
  name: 'Course',
  data () {
    return {

    }
  },
  created () {
    console.log(this.$route.params.id);
  },
  components: {
    'Header': Header,
    'CourseInfo': CourseInfo,
    'CourseOutline': CourseOutline
  }
}
</script>

<style lang="css">
.course-main {
  height: 100%;
  background-color: #f8f8f9;
}
.content-wrap {
  height: 100%;
  background-color: #f8f8f9;
}
.course-content {
  height: 100%;
  width: 1175px;
  margin: 0 auto;
  padding: 15px 0;
}
.float-clear {
  clear: both;
}
</style>
