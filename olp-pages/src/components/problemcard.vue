<template lang="html">
  <div class="problemcard-wrap">
    <div class="problemcard-title-wrap">
      <p>答题卡</p>
    </div>
    <div class="problemcard-nav-wrap">
      <div id="p1" class="problemcard-nav problemcard-cur" @click="pSelected($event)">
        <p>1</p>
      </div>
      <div id="p2" class="problemcard-nav problemcard-no" @click="pSelected($event)">
        <p>2</p>
      </div>
      <div class="float-clear">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProblemCard',
  data () {
    return {

    }
  },
  methods: {
    pSelected: function (e) {
      var pid = e.path[1].attributes["id"].value;
      var ele = document.getElementById(pid);
      var className = ele.attributes["class"].value;
      if (className.indexOf('problemcard-cur')) {
      }
    }
  }
}
</script>

<style lang="css">
.problemcard-wrap {
  background-color: #fff;
  padding: 15px 20px;
  margin-bottom: 15px;
}
.problemcard-title-wrap>p {
  text-align: left;
  font-size: 1.2rem;
  font-weight: bold;
}
.problemcard-nav-wrap {
  padding: 10px 0;
}
.problemcard-nav {
  float: left;
  width: 41px;
  height: 41px;
  /* background-color: #2d8cf0; */
  margin-right: 5px;
  /* color: #fff; */
}
.problemcard-nav>p, .problemcard-yes>p, .problemcard-no>p {
  font-size: 1.2rem;
  color: inherit;
  font-weight: bold;
  padding: 8px 0;
}
.problemcard-cur, .problemcard-yes {
  background-color: #2d8cf0;
  color: #fff;
}
.problemcard-no {
  background-color: #fff;
  color: #2d8cf0;
}
.problemcard-correct {
  background-color: #19be6b;
  color: #fff;
}
.problemcard-false {
  background-color: #ed3f14;
  color: #fff;
}
</style>
