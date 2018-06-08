<template lang="html">
  <div class="importstudent-wrap">
    <div class="import-input-wrap">
      <p><span style="padding-right: 10px;">学生学号</span><Input v-model="studentId" style="width: 200px; padding-right: 10px;" /><Button type="success" @click="handleImport">确认添加</Button></p>
    </div>
    <div class="student-table" style="margin-top: 30px;">
      <Table :columns="column" :data="table" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ImportStudent',
  data () {
    return {
      studentId: '',
      column: [
        {
          title: '序号',
          key: 'number'
        },
        {
          title: '学号',
          key: 'uid'
        }
      ],
      table: [],
      courseId: this.$route.params.courseid
    }
  },
  mounted () {
    axios.get("http://"+this.BASEURL+"/studentNameList?courseId="+this.courseId).then(function(res) {
      console.log(res);
      this.table = res.data;
    }.bind(this));
  },
  methods: {
    handleImport: function() {
      var re = /^[0-9]+.?[0-9]*/;
      if (this.studentId === '') {
        alert("请填写学生学号！");
      } else if (!re.test(this.studentId) || this.studentId.length != 10) {
        alert ("请输入正确的学号！");
      } else {
        for (var i = 0; i < this.table.length; i++) {
          if (this.table[i].uid === this.studentId) {
            alert ("该学生已存在！");
            return;
          }
        }
        var d = {
          courseId: this.courseId,
          uid: this.studentId
        }
        axios.post("http://"+this.BASEURL+"/importStudent",d).then(function(res) {
          console.log(res);
          if (res.data.success) {
            alert ("添加成功！");
            axios.get("http://"+this.BASEURL+"/studentNameList?courseId="+this.courseId).then(function(res) {
              this.table = res.data;
            }.bind(this));
          } else {
            alert(res.data.reason);
          }
        }.bind(this));
      }
    }
  }
}
</script>

<style lang="css">
.importstudent-wrap {
  width: 860px;
  float: right;
  text-align: left;
  padding: 20px 15px;
  background-color: #fff;
}
</style>
