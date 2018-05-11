<template lang="html">
  <div class="courseoutlinesmall-list">
    <div class="courseoutlinesmall-item courseoutlinesmall-item-mid">
      <div class="courseoutlinesmall-item-section-info">
        <div class="courseoutlinesmall-item-section-number section-number-off">
          <p>1</p>
        </div>
        <div class="courseoutlinesmall-item-section-title">
          <p>Java 基础 1</p>
        </div>
        <div class="courseoutlinesmall-item-section-other">
          <p>18:30</p>
        </div>
        <div class="float-clear">
        </div>
      </div>
      <div class="courseoutlinesmall-item-section-description">
        <div class="courseoutlinesmall-item-section-description-wrap">
          <p>本课时介绍移动开发操作系统的发展历史，对 Android 的各个版本逐一回顾，简单讲解 Android 系统的构成，帮助大家快速了解 Android 体系的整体情况</p>
        </div>
      </div>
    </div>
    <div class="courseoutlinesmall-item courseoutlinesmall-item-mid">
      <div class="courseoutlinesmall-item-section-info">
        <div class="courseoutlinesmall-item-section-number section-number-on">
          <p>2</p>
        </div>
        <div class="courseoutlinesmall-item-section-title">
          <p>Java 基础 2</p>
        </div>
        <div class="courseoutlinesmall-item-section-other">
          <p>18:30</p>
        </div>
        <div class="float-clear">
        </div>
      </div>
      <div class="courseoutlinesmall-item-section-description">
        <div class="courseoutlinesmall-item-section-description-wrap">
          <p>本课时介绍移动开发操作系统的发展历史，对 Android 的各个版本逐一回顾，简单讲解 Android 系统的构成，帮助大家快速了解 Android 体系的整体情况</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseOutlineSmall',
  data () {
    return {

    }
  }
}
</script>

<style lang="css">
.courseoutlinesmall-list {
  width: 415px;
  height: 489px;
  overflow-y: auto;
  padding: 10px 5px 0;
}
.courseoutlinesmall-item-mid {
  padding-bottom: 15px;
}
.courseoutlinesmall-item-section-info {
  padding-bottom: 5px;
}
.courseoutlinesmall-item-section-number {
  float: left;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  padding: 1px 0 2px;
}
.section-number-off {
  background-color: #bbbec4;
}
.section-number-on {
  background-color: #2d8cf0;
}
.courseoutlinesmall-item-section-number>p {
  padding: 1px 0;
  font-weight: bold;
  color: #fff;
}
.courseoutlinesmall-item-section-title {
  float: left;
}
.courseoutlinesmall-item-section-title>p {
  padding-left: 10px;
  font-size: 1.1rem;
  white-space: pre-wrap;
}
.courseoutlinesmall-item-section-other {
  float: right;
}
.courseoutlinesmall-item-section-other>p {
  padding: 2px 0 3px;
  color: #80848f;
}
.courseoutlinesmall-item-section-description {
  padding-left: 30px;
}
.courseoutlinesmall-item-section-description-wrap>p {
  text-align: left;
  color: #80848f;
}
</style>
