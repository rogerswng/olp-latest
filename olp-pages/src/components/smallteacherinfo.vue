<template lang="html">
  <div class="smallteacherinfo">
    <div class="smallteacherinfo-avatar">
      <Avatar type="person" size="small" />
    </div>
    <div class="smallteacherinfo-name">
      <p>老师 A</p>
    </div>
    <div class="float-clear">
    </div>
  </div>
</template>

<script>
export default {
  name: 'SmallTeacherInfo',
  data () {
    return {

    }
  }
}
</script>

<style lang="css">
.smallteacherinfo {
  position: relative;
}
.smallteacherinfo-avatar {
  float: left;
}
.smallteacherinfo-name {
  position: absolute;
  left: 34px;
  top: 50%;
  transform: translateY(-9px);
}
.smallteacherinfo-name>p {
  white-space: pre-wrap;
  color: #80848f;
}
.float-clear {
  clear: both;
}
</style>
