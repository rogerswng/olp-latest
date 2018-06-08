<template lang="html">
  <div class="teachertopicedit-content-wrap">
    <div class="teachertopicedit-content">
      <div class="teachertopicedit-title">
        <p style="padding-top: 10px; font-size: 1.5em; font-weight: bold;" v-if="this.type === 'create'">新增章节</p>
        <p style="padding-top: 10px; font-size: 1.5em; font-weight: bold;" v-else-if="this.type === 'edit'">编辑章节</p>
        <p style="padding-top: 5px; font-size: 1.2em; color: #80848f;">{{title}}</p>
      </div>
      <div class="teachertopicedit-detail">
        <div class="teachertopicedit-input-wrap" style="padding: 15px 20px; float: left;">
          <span style="padding-right: 10px;">主题名</span>
          <Input v-model="topicTitle" placeholder="主题名" style="width: 500px;" />
        </div>
        <div class="float-clear">
        </div>
      </div>
      <div class="button-wrap" style="float: right; padding: 0 20px 20px;">
        <Button type="error" @click="handleCancel">取消</Button>
        <Button type="success" @click="handleSave">保存</Button>
      </div>
      <div class="float-clear">
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TeacherTopicEdit',
  data () {
    return {
      courseid: '',
      topicid: '',
      type: '',
      title: '',
      topicTitle: ''
    }
  },
  methods: {
    handleCancel: function () {
      // console.log(this.$route.params);
      this.$router.push({path: '/teachermain/courseEdit/'+this.courseid});
      // window.location.reload();
    },
    handleSave: function () {
      console.log(this.topicTitle);
      if (this.type === 'create') {
        var d = {
          courseId: this.courseid,
          title: this.topicTitle
        }
        axios.post("http://"+this.BASEURL+"/createTopic", d).then(function(res) {
          if (res.data.state === 'success') {
            alert("保存成功，topicid"+res.data.topic_id);
            this.$router.push({path: '/teachermain/courseEdit/'+this.courseid});
          }
        }.bind(this));
      } else if (this.type === 'edit') {
        // alert('edit');
        var d = {
          topicId: this.topicid,
          topicTitle: this.topicTitle
        }
        axios.put("http://"+this.BASEURL+"/editTopic", d).then(function(res) {
          if(res.data.success) {
            alert("保存成功!");
            this.$router.push({path: '/teachermain/courseEdit/'+this.courseid});
          }
        }.bind(this));
      }
      // alert("保存成功！");
      // this.$router.push({path: '/teachermain/courseEdit/'+this.courseid});
      // // this.$router.push({path: '/teachermain/courseEdit/'+this.id});
      // if (this.type = )
    },
    initComp: function () {
      // console.log(this.$route.name)
      if (this.$route.name.indexOf("TeacherTopicCreate") != -1) {
        this.courseid = this.$route.params.courseid;
        this.type = "create";
        axios.get("http://"+this.BASEURL+"/courseTitle?courseId="+this.courseid).then(function(res) {
          this.title = res.data.title;
        }.bind(this));
        this.topicTitle = "";
      } else if (this.$route.name.indexOf("TeacherTopicEdit") != -1) {
        this.courseid = this.$route.params.courseid;
        this.topicid = this.$route.params.topicid;
        this.type = "edit";
        axios.get("http://"+this.BASEURL+"/courseTitle?courseId="+this.courseid).then(function (res) {
          this.title=res.data.title;
        }.bind(this));
        axios.get("http://"+this.BASEURL+"/topicTitle?topicId="+this.topicid).then(function(res) {
          this.topicTitle = res.data.title
        }.bind(this));
        // this.topicTitle = "DataLoadfromRemoteServer";
      }
      // Data Request and load
    }
  },
  mounted () {
    console.log(this.$route);
    this.initComp();
  }
}
</script>

<style lang="css">
.float-clear {
  clear: both;
}
.teachertopicedit-content-wrap {
  width: 875px;
  float: right;
  background-color: #f8f8f9;
  padding: 0 10px;
}
.teachertopicedit-content {
  background-color: #fff;
  /* padding: 0 10px; */
}
.teachertopicedit-title {
  text-align: left;
  padding-left: 20px;
}
</style>
