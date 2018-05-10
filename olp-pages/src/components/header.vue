<template>
  <div class="header-wrap">
    <div class="header">
      <div class="header-label">
        <p>Online Learning</p>
      </div>
      <div class="userInfo">
        <div class="avatar">
          <Avatar icon="person" size="large" />
        </div>
        <div class="username">
          <p>{{ username }}</p>
        </div>
      </div>
      <div class="float-clear">
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Header',
    data () {
      return {
        username: this.$getCookie('username')
      }
    }
  }
</script>

<style>
.header-wrap {
  width: 100%;
  background-color: #ffffff;
  border-bottom: 1px solid #dddee1;
}
.header {
  width: 1175px;
  margin: 0 auto;
  padding: 10px 0;
}
.header-label {
  float: left;
  display: inline-block;
  vertical-align: middle;
  padding: 5px 0;
}
.header-label>p {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2d8cf0;
  width: 12rem;
}
.userInfo {
  float: right;
  display: inline-block;
  vertical-align: middle;

}
.avatar {
  display: inline-block;
}
.username {
  display: inline-block;
  margin-left: 0.5rem;
}
.float-clear {
  clear: both;
}
</style>
