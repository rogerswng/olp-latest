<template lang="html">
  <div class="courseoutline-main">
    <div class="courseoutline-content">
      <div class="courseoutline-label">
        <p>课时列表</p>
      </div>
      <div class="courseoutline-topic">
        <div class="courseoutline-topic-title">
          <p>第 1 课 · 初识 Java</p>
        </div>
        <div class="courseoutline-section-list">
          <div class="courseoutline-section-item">
            <div class="section-info">
              <div class="section-number section-number-off">
                <p>1</p>
              </div>
              <div class="section-title">
                <p>Java 简介</p>
              </div>
              <div class="section-other video-time-wrap">
                <p>18:30</p>
              </div>
              <div class="float-clear">
              </div>
            </div>
            <div class="section-description">
              <p>本课时介绍移动开发操作系统的发展历史，对 Android 的各个版本逐一回顾，简单讲解 Android 系统的构成，帮助大家快速了解 Android 体系的整体情况</p>
            </div>
          </div>
          <div class="courseoutline-section-item">
            <div class="section-info">
              <div class="section-number section-number-finish">
                <p>2</p>
              </div>
              <div class="section-title">
                <p>Java 简介</p>
              </div>
              <div class="section-other video-time-wrap">
                <p>18:30</p>
              </div>
              <div class="float-clear">
              </div>
            </div>
            <div class="section-description">
              <p>本课时介绍移动开发操作系统的发展历史，对 Android 的各个版本逐一回顾，简单讲解 Android 系统的构成，帮助大家快速了解 Android 体系的整体情况</p>
            </div>
          </div>
          <div class="courseoutline-section-item">
            <div class="section-info">
              <div class="section-number section-number-learning">
                <p>3</p>
              </div>
              <div class="section-title">
                <p>Java 简介</p>
              </div>
              <div class="section-other video-time-wrap">
                <p>18:30</p>
              </div>
              <div class="float-clear">
              </div>
            </div>
            <div class="section-description">
              <p>本课时介绍移动开发操作系统的发展历史，对 Android 的各个版本逐一回顾，简单讲解 Android 系统的构成，帮助大家快速了解 Android 体系的整体情况</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseOutline',
  data () {
    return {

    }
  },
  created () {
    console.log(this.$route.params.id);
  }
}
</script>

<style lang="css">
.float-clear {
  clear: both;
}
.courseoutline-main {
  height: 100%;
  background-color: #ffffff;
  width: 860px;
  float: right;
}
.courseoutline-content {
  /* height: 100%; */
  padding: 15px 20px;
}
.courseoutline-label {
  padding-bottom: 10px;
}
.courseoutline-label>p {
  text-align: left;
  font-size: 1.2rem;
  font-weight: bold;
  color: #80848f;
}
.courseoutline-topic-title {
  background-color: #2d8cf0;
  padding: 5px 10px;
}
.courseoutline-topic-title>p {
  text-align: left;
  color: #ffffff;
  font-weight: bold;
  white-space: pre-wrap;
}
.courseoutline-section-item {
  width: 820px;
  /* padding-top: 10px; */
  padding: 10px 10px;
}

.section-info {
  padding-bottom: 5px;
}
.section-number {
  float: left;
  height: 25px;
  width: 25px;
  border-radius: 50%;
  padding: 3px 0 4px;
}
.section-number-off {
  background-color: #bbbec4;
}
.section-number-finish {
  background-color: #19be6b;
}
.section-number-learning {
  background-color: #2d8cf0;
}
.section-number>p {
  /* font-size: 1rem; */
  font-weight: bold;
  color: #ffffff;
}
.section-title {
  float: left;
  padding: 1px 0 1px 10px;
}
.section-title>p {
  white-space: pre-wrap;
  font-size: 1.1rem;
  color: #495060;
}
.section-other {
  float: right;
}
.video-time-wrap {
  padding: 3px 0 4px;
}
.video-time-wrap>p {
  color: #80848f;
}

.section-description {
  padding-left: 35px;
}
.section-description>p {
  text-align: left;
  color: #80848f;
}
</style>
